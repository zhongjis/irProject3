import json

# this class manipulates the bookkeeping file
class BookkeepingProcesser:

    def __init__(self):
        self.file_count = 0 # number of total files
        self.keys = [] 
        self.json_bookkeeping = {} # json object for bookkeeping

    # this method reading the bookkeeping file and load the file into a dict
    def read_bookkeeping(self):

        # setting up files and get ready to process 
        file_bookkeeping = open('WEBPAGES_RAW/bookkeeping.json')
        json_bookkeeping = json.load(file_bookkeeping)

        # processing
        for l in json_bookkeeping:
            self.file_count += 1
            self.keys.append(l.encode("utf-8"))

            # for test purpose, will only read the first 100 items
            # TODO: need to be removed upon finish
            if self.file_count >= 2000:
                break

        self.json_bookkeeping = json_bookkeeping

        # wrapping up
        file_bookkeeping.close()
        print("Total files: " + str(self.file_count))


    # this method will translate page path to url
    def translate_path_to_url(self, path):
        return self.json_bookkeeping[path]