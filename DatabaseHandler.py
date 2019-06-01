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

        cursor = self.mycol.find()

        for record in cursor:
                print(record)
                print("\n")



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
        path_dict = {}
        temp_dict = {}
        sorted_dict = {}
        valid_entry_dict = self.search_valid(query) 
        # valid_entry_dict[token] = {page_path : tdidf}
        
        for i in valid_entry_dict.items():
            print(i)

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

        print("path dict")
        for i in path_dict.items():
            print(i)

        for k, v in path_dict.items():
            score = 0
            for i in v:
                score += v[i]
            score_dict[k] = score
            # the search result will only present the top 10
            sorted_dict = sorted(score_dict, key=score_dict.get, reverse=True)[:10]
        print("sorted dict")
        # for i in sorted_dict.items():
        #     print(i)
        print(sorted_dict)

        result = sorted_dict
        return result