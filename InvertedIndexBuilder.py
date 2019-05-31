

# this class will build a inverted index
# the index will be written into index_record.txt
class InvertedIndexBuilder:

    def __init__(self):
        self.inverted_index = {} # dict[token] = {page_path : occurance}


    # this method will generate a dict of inverted index 
    # that each item follows the format dict[token] = {page_path: tf}
    # @para [tokens] dict[page_path] = {token: occurance}
    def build(self, tokens):
        for page_path in tokens:
            for token in tokens[page_path]:
                if token not in self.inverted_index:
                    self.inverted_index[token] = {page_path:tokens[page_path][token]}
                else:
                    self.inverted_index[token].update({page_path:tokens[page_path][token]})


        for i in self.inverted_index:
            print(i, self.inverted_index[i])


    # this method will caculate the frequency
    def caculate(self, total_doc_number):
        # calculate tf for all the tokens
        
        # path_and_tf_dict[page_path] = occurence
        for token, path_and_tf_dict in self.inverted_index.items():
            _nmbr_of_doc_with_tkn = len(path_and_tf_dict.keys()) # number of times this token appeared in the corpus
            _inversed_doc_frequency = float(total_doc_number) / _nmbr_of_doc_with_tkn

            for path, _token_frequency in path_and_tf_dict.items():
                _tf_idf = _token_frequency * _inversed_doc_frequency
                # replace token occurence with _tf_idf
                # new inverted_index format:
                # dict[token] = {page_path : tf_idf}
                path_and_tf_dict[path] = _tf_idf

        index_record = open('inverted_index.txt', 'w')

        for token, path_and_tf_dict in sorted(self.inverted_index.items()):
            index_record.write(str(token) + str(path_and_tf_dict) + "\n\n")

        print('the inverted index table is saved to index_record.txt')
        print('Total unique words: ' + str(len(self.inverted_index)))

        return self.inverted_index