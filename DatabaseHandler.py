import pymongo
from ast import literal_eval

# this class handles all actions about the database
# database used here is Mongodb
class DatabaseHandler:

    def __init__(self):
        try:
            self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            print('[Success] MongoDB connected')
        except:
            print('[Fail] Cannot connect to MongoDB')


    def connect(self, dbname, colname, keep_old_collection = False):
        # connect to db instance
        self.mydb = self.myclient[dbname]

        # create table
        collist = self.mydb.list_collection_names()
        if colname in collist and keep_old_collection == False:
            print("[Warning] The collection exists. dropping the old collection")
            try:
                self.mydb.drop_collection(colname)
                print("[Success] Old collection dropped")
            except:
                print("[Fail] Cannot drop old collection")
        
        self.mycol = self.mydb['inverted_index_table']
        print("[Success] Created new collection .." + colname + ".. under " + dbname)


    # this method handles data insertion
    def insert(self, item):
        couter = 0
        trigger = 1000

        container = dict()

        for i in item:
            container[i] = item[i]
            if couter >= trigger:
                self.mycol.insert_one(container)
                container = dict()
                couter = 0
            couter += 1

        self.mycol.insert_one(container)


    # this method will seach the database for the documents including the query term. the result is not ranked
    def search_valid(self, query):
        good_records = dict() # files that includes query
        col_items = self.mycol.find()
        for col_item in col_items:
            for word, postings in col_item.items():
                for term in query:
                    if term in word or term == word: 
                        good_records[word] = postings
        return good_records

    def search(self, query):
        score_dict = {}
        path_dict = {} # (b'0/2', {'home': 3.508771929824561, 'informatics': 7.6923076923076925})
        temp_dict = {}
        valid_entry_dict = self.search_valid(query) 
        # valid_entry_dict[token] = {page_path : tdidf}

        for token, postings in valid_entry_dict.items():
            # turning postings from bytes to dict
            postings = postings.decode("utf-8")
            postings = literal_eval(postings)
            
            for path, tdidf in postings.items():
                if path not in path_dict:
                    temp_dict = {token:tdidf}
                    path_dict[path] = temp_dict
                else:
                    # technically won't happen cuz there's no duplication
                    temp_dict = {token:tdidf}
                    # TODO suppose to addon
                    path_dict[path].update(temp_dict)

        # calculating the final score
        for path, postings in path_dict.items():
            score = 0
            for key in postings:
                score += postings[key]
            score_dict[path] = score

        # get top 20 keys from score_dict, highest first
        result = sorted(score_dict, key=score_dict.get, reverse=True)[:20]

        return result