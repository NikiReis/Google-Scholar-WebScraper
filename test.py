import pandas as pd
import selenium 
from bs4 import BeautifulSoup
import resquests



def data_wragling():
	url = requests.get('https://epic.gsfc.nasa.gov/api/natural').json
	print(url)

if __name__ == '__main__':
	data_wragling()
