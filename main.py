# Zhongjie Shen 26688124
from Tokenizer import Tokenizer
from BookkeepingProcesser import BookkeepingProcesser


if __name__ == "__main__":
    driver = BookkeepingProcesser()
    driver.read_bookkeeping()

    tokenizer = Tokenizer(driver.keys, driver.file_count)
    tokenizer.start()