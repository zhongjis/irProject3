from nltk.corpus import stopwords 

# add removing stop words from query

class UserInputHandler:

    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

        self.original_query = ""
        self.query_token_list = []

    def ask_query(self):
        self.original_query = input("Please input your query: ")    
        return self.original_query

    # this method will remove stop_words from the query
    def remove_stop_words(self):
        tokens = self.original_query.lower().split()
        self.query_token_list = [i for i in tokens if i not in self.stop_words]
        return self.query_token_list