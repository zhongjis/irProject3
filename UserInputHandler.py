
class UserInputHandler:

    def __init__(self):
        self.original_query = ""

    def ask_query(self):
        self.original_query = input("Please input your query: ")    
        return self.original_query
