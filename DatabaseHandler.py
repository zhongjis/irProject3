import pymongo

# this class handles all actions about the database
# database used here is Mongodb
class DatabaseHandler:

    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        print('[Success] MongoDB connected')

    def connect(self, dbname, colname):
        self.mydb = self.myclient["INF141_assignment_3"]
        self.mycol = self.mydb['inverted_index_table']

    def insert(self):
        pass