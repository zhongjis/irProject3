import pymongo

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


    def insert(self, item):
        couter = 0
        trigger = 2000

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
            for k, v in col_item.items():
                if query in k or query == k: 
                    good_records[k] = v
        return good_records