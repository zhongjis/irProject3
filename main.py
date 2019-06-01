# Zhongjie Shen 26688124
import time
from ast import literal_eval

from Tokenizer import Tokenizer
from BookkeepingProcesser import BookkeepingProcesser
from InvertedIndexBuilder import InvertedIndexBuilder
from DatabaseHandler import DatabaseHandler
from UserInputHandler import UserInputHandler


if __name__ == "__main__":
    if_build_index = input("[IMPORTANT] Do you want to build the index? [Yes/No]")

    if if_build_index == "Yes":

        print ("[Message] Sure, start building")

        # process bookkeeping file
        print("[Progress] Start reading bookkeeping file")

        driver = BookkeepingProcesser()
        driver.read_bookkeeping()

        print("[Progress] Finished reading bookkeeping file")

        # tokenize the raw html files generated from driver
        print("[Progress] Start index building...")
        start = time.time()

        tokenizer = Tokenizer(driver.keys, driver.file_count)
        tokenizer.start()

        # rename class variables for better expression
        total_document_number = driver.file_count
        tokens_dict = tokenizer.tokenized

        # building inverted_index
        inverted_index_builder = InvertedIndexBuilder()
        inverted_index_builder.build(tokens_dict)
        inverted_index_builder.caculate(total_document_number)
        inverted_index = inverted_index_builder.getInvertedIndex()

        # index building report
        end = time.time()
        time_used = end - start
        print("[Progress] Finished index building, used " + str(time_used) + "s")

        # setting up MongoDB
        db = DatabaseHandler()
        db.connect("INF141_assignment_3", "inverted_index_table")

        # inserting items in inverted_index
        print("[Progress] Start inserting entries into database")
        start = time.time()

        ready_to_insert = {k: str(v).encode("utf-8") for k,v in inverted_index.items()}
        db.insert(ready_to_insert)

        end = time.time()
        time_used = end - start
        print("[Progress] Finished database insertion, used " + str(time_used) + "s")

    else:
        # set up db and bookkeeping processor
        db = DatabaseHandler()
        db.connect("INF141_assignment_3", "inverted_index_table", True)

        driver = driver = BookkeepingProcesser()
        driver.read_bookkeeping()

        # query handling
        inputHandlr = UserInputHandler()
        query = inputHandlr.ask_query().lower()
        query_token = inputHandlr.remove_stop_words()

        # search
        output = db.search(query_token)

        print("[Message]Here's the top 10 results (highest first):")

        for i in output:
            path = i.decode('utf-8')
            url = driver.translate_path_to_url(path)
            print(url)
