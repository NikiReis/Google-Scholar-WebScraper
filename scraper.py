import csv
from bs4 import BeautifulSoup
import requests

url = requests.get('').content


soup = BeautifulSoup(url, 'html.parser')
lista = soup.find_all('div', class_="gs_ri")

datalist = []
data = {}
fields = ['Book','Authors','Journal','Year','Publisher','Link']

for item in lista:
  try:

    title = item.find("h3", class_='gs_rt').text.strip()
    if '[PDF]' in title or '[HTML]' in title or '[LIVRO]' in title:
      title = title.replace('[PDF]', '').replace('[HTML]', '').replace('[LIVRO][B]', '')
    data['Book'] = title

    authors = item.find("div", class_="gs_a").text.split('-')[0]
    data['Authors'] = authors

    journal = item.find("div", class_="gs_a").text.split('-')[1].strip().split(', ')[0]
    data['Journal'] = journal

    year = item.find("div", class_="gs_a").text.split("-")[1].strip().split(', ')[1]
    data['Year'] = year

    publisher = item.find("div", class_="gs_a").text.split("-")[2].strip().split()[0]
    data['Publisher'] = publisher

    link = item.find("a", href=True)
    if link:
      data['Link'] = link['href']
    else:
      data['Link'] = ''

  except IndexError:

    title = item.find("h3", class_='gs_rt').text.strip()

    if '[PDF]' in title or '[HTML]' in title or '[LIVRO]' in title:
      title = title.replace('[PDF]', '').replace('[HTML]', '').replace('[LIVRO][B]', '')
    data['Book'] = title

    authors = item.find("div", class_="gs_a").text.split('-')[0]
    data['Authors'] = authors

    journal_year_publisher = item.find('div', class_='gs_a').text.split('-')
    if len(journal_year_publisher) >= 3:
      journal = journal_year_publisher[1].strip().split(',')[0]
      year = journal_year_publisher[1].strip().split(',')[-1].strip()
      publisher = journal_year_publisher[2].strip().split()[0]
    else:
      journal = '****'
      year = '****'
      publisher = '****'

    data['Journal'] = journal
    data['Year'] = year
    data['Publisher'] = publisher

    link = item.find("a", href=True)
    if link:
      data['Link'] = link['href']
    else:
      data['Link'] = ''

  datalist.append(data.copy())
  data.clear()

with open('data_set.csv', 'a', newline='') as f:
  writer = csv.DictWriter(f, fieldnames=fields)
  writer.writerows(datalist)

