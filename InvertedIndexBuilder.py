

# this class will build a inverted index
# the index will be written into index_record.txt
class InvertedIndexBuilder:

    def __init__(self):
        self.inverted_index = {}

    # this will build a index file
    def build(self, token_frequency, total_doc_number):
        # calculate tf for all the tokens
        
        for token, path_with_tf_dict in token_frequency.items():
            _doc_token - len(path_with_tf_dict.keys())
            _inversed_doc_frequency = float(total_doc_number) / _doc_token

            for url, _token_frequency in _inversed_doc_frequency.items():
                _tf_idf = _token_frequency * _inversed_doc_frequency
                path_with_tf_dict[url] = _tf_idf

        print(token_frequency.items())

        index_record = open('index_record.txt', 'w')

        for token, path_with_tf_dict in sorted(token_frequency.items()):
            index_record.write(str(token) + str(path_with_tf_dict) + "\n")

        print('generated index_record.txt')
        print('Total unique entries: ' + str(len(token_frequency)))

        return token_frequency