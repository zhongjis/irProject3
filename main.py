# Zhongjie Shen 26688124
from Tokenizer import Tokenizer
from BookkeepingProcesser import BookkeepingProcesser
from InvertedIndexBuilder import InvertedIndexBuilder
from DatabaseHandler import DatabaseHandler


if __name__ == "__main__":

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
