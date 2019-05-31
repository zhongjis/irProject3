from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer

# this class handling the file tokenizing
class Tokenizer:

    def __init__(self, keys, total):
        self.paths = keys
        self.total = total
        self.tokenized = {} # dict[page_path] = {word: occurance}

    # this method will initialize the tokenizing process
    def start(self):
        count = 0
        for path in self.paths:
            self.tokenized[path] = self.tokenize(path.decode("utf-8"))
            count += 1
            print("Tokenizing: " + str(path) + "\t" + str(count) + " out of " + str(self.total))

        # for i in self.tokenized:
        #     print(i, self.tokenized[i])

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