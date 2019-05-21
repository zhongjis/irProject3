import json
import re
from bs4 import BeautifulSoup

def ask_input() -> str:
	print("please enter your query: ")
	result = input()
	return result

def run_query(bookkeeping, query):
	# this function will run the query over all the pages in bookkeeping
	result = []
	for d in bookkeeping:
		page = open('WEBPAGES_RAW/'+d)
		soup = BeautifulSoup(page, 'html.parser')
		# test = soup.findAll(text = re.compile(query[:3]))
		test = re.compile(query[:3])
		print(test.fullmatch(query))

		if (test.fullmatch(query)):
			print(bookkeeping[d])
			result.append(bookkeeping[d])
		page.close()
	return result

def main():
	# load indexs
	file = open('WEBPAGES_RAW/bookkeeping.json')
	bookkeeping = json.load(file)

	# input query
	query = ask_input()

	# run query over pages
	result = run_query(bookkeeping, query)

	print(result)

	# wrapping up
	file.close()

if __name__ == "__main__":
	main()

