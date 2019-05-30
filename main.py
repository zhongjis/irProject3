import json
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

# beginning of Milestone 1


# this class manipulates the bookkeeping file
class BookkeepingProcesser:

    def __init__(self):
        self.file_count = 0
        self.keys = []
        self.json_bookkeeping = {}

    # this function reading the bookkeeping file and load the file into a dict
    def read_bookkeeping(self):

        # setting up files and get ready to process 
        file_bookkeeping = open('WEBPAGES_RAW/bookkeeping.json')
        json_bookkeeping = json.load(file_bookkeeping)

        # processing
        for l in json_bookkeeping:
            self.file_count += 1
            self.keys.append(l.encode("utf-8"))
        self.json_bookkeeping = json_bookkeeping

        # wrapping up
        file_bookkeeping.close()
        print("Total files: " + str(self.file_count))


# this class handling the file tokenizing
class Tokenizer:

    def __init__(self, keys, total):
        self.paths = keys
        self.tokenized = {}
        self.total = total

    # this function will initialize the tokenizing process
    def start(self):
        count = 0
        for path in self.paths:
            self.tokenized[path] = self.tokenize(path.decode("utf-8"))
            count += 1
            print("Tokenizing: " + str(path) + "\t" + str(count) + " out of " + str(self.total))

    def tokenize(self, file_path):
        tokenizer = RegexpTokenizer(pattern=r'[a-zA-Z0-9]+')
        html = open("WEBPAGES_RAW/" + file_path).read()
        soup = BeautifulSoup(html, "lxml")

        # house cleaning, remove tags of script and styles
        for i in soup(["script", "style"]):
            i.extract() 

        soup = soup.get_text()

        # tokenizing
        _valid_tokens = {}
        for word in tokenizer.tokenize(soup):
            if word.lower() in _valid_tokens.keys():
                _valid_tokens[word.lower()] += 1
            else:
                _valid_tokens[word.lower()] = 1

        return _valid_tokens


if __name__ == "__main__":
    driver = BookkeepingProcesser()
    driver.read_bookkeeping()

    tokenizer = Tokenizer(driver.keys, driver.file_count)
    tokenizer.start()
    tokens_dict = tokenizer.tokenized

    token_dict_frequency = {} # dict[word] = pair(url, tf)

    for i in tokens_dict:
        for word in tokens_dict[i]:
            if word not in token_dict_frequency:
                token_dict_frequency[word] = {url:token_dict[url][word]}
            else:
                token_dict_frequency[word].update({url:token_dict[url][word]})

    print(token_dict_frequency)




