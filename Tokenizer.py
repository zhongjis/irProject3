from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer

# this class handling the file tokenizing
class Tokenizer:

    def __init__(self, keys, total):
        self.paths = keys
        self.total = total
        self.tokenized = {}
        self.tokenized_frequency = {} # dict[word] = {page_path : occurance}

    # this method will initialize the tokenizing process
    def start(self):
        count = 0
        for path in self.paths:
            self.tokenized[path] = self.tokenize(path.decode("utf-8"))
            count += 1
            print("Tokenizing: " + str(path) + "\t" + str(count) + " out of " + str(self.total))

            # testing control. need to be removed when finished
            if count >= 200:
                print("testing until 200")
                break

        self.tokenize_update_frequency()

        # for i in self.tokenized_frequency:
        #     print(i, self.tokenized_frequency[i])

        for i in self.tokenized:
            print(i, self.tokenized[i])

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

    # this method will generate a dict that each item 
    # follows the format dict[word] = pair(page_path, tf)
    def tokenize_update_frequency(self):
        for page_path in self.tokenized:
            for word in self.tokenized[page_path]:
                if word not in self.tokenized_frequency:
                    self.tokenized_frequency[word] = {page_path:self.tokenized[page_path][word]}
                else:
                    self.tokenized_frequency[word].update({page_path:self.tokenized[page_path][word]})