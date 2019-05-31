# Zhongjie Shen 26688124
from Tokenizer import Tokenizer
from BookkeepingProcesser import BookkeepingProcesser
from InvertedIndexBuilder import InvertedIndexBuilder
import pymongo


if __name__ == "__main__":

    # setting up MongoDB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    print('[Success] MongoDB connected')

    mydb = myclient["INF141_assignment_3"]
    mycol = mydb['inverted_index_table']

    # process bookkeeping file
    driver = BookkeepingProcesser()
    driver.read_bookkeeping()

    # tokenize the raw html files generated from driver
    tokenizer = Tokenizer(driver.keys, driver.file_count)
    tokenizer.start()

    # rename class variables for better expression
    total_document_number = driver.file_count
    tokens_dict = tokenizer.tokenized

    # building inverted_index
    inverted_index_builder = InvertedIndexBuilder()
    inverted_index_builder.build(tokens_dict)
    inverted_index = inverted_index_builder.caculate(total_document_number)
