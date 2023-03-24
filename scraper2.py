import csv
from bs4 import BeautifulSoup
import requests
import os


FIELDS = ['Book', 'Authors', 'Jornal', 'Year', 'Publisher', 'Link']
JUNK = [['… ', ' ', ' …', '…'], ['[HTML]', '[PDF]', '[LIVRO][B]', '[BOOK][B]']]
datalist = []
data = {}


def filtering(lista):

    try:

        for item in lista:

            book = item.find('h3', class_='gs_rt').text.strip()
            if JUNK[1][0] in book or JUNK[1][1] in book or JUNK[1][2] in book:
                book = book.replace(JUNK[1][0], '').replace(JUNK[1][1], '').replace(JUNK[1][2], '').replace(JUNK[1][3], '')

            item_length = item.find('div',class_='gs_a').text.split('-')
            if len(item_length) >= 3:

                authors = item.find('div', class_='gs_a').text.strip().split('-')[0]
                if JUNK[0][0] in authors or JUNK[0][1] in authors or JUNK[0][2] in authors:
                    authors = authors.replace(JUNK[0][0], '').replace(JUNK[0][1], '').replace(JUNK[0][2], '')


                jornal = item.find("div", class_="gs_a").text.strip().split('-')[1].strip().split(',')[0]
                if JUNK[0][0] in jornal or JUNK[0][1] in jornal or JUNK[0][2] in jornal or JUNK[0][3] in jornal:
                    jornal = jornal.replace(JUNK[0][0], '').replace(JUNK[0][1], '').replace(JUNK[0][2], '').replace(
                        JUNK[0][3],
                        '')

                year = item.find("div", class_='gs_a').text.strip().split('-')[1].split()[-1]

                publisher = item.find("div", class_="gs_a").text.strip().split('-')[2].strip()
                if JUNK[0][0] in publisher or JUNK[0][1] in publisher or JUNK[0][2]:
                    publisher = publisher.replace(JUNK[0][0], '').replace(JUNK[0][1], '').replace(JUNK[0][2], '')

            
            else:

                authors = item.find('div', class_='gs_a').text.split('-')[0].strip()
                if JUNK[0][0] in authors or JUNK[0][1] in authors or JUNK[0][2] in authors:
                    authors = authors.replace(JUNK[0][0], '').replace(JUNK[0][1], '').replace(JUNK[0][2], '')


                publisher = item.find('div', class_='gs_a').text.split('-')[-1].strip()
                if JUNK[0][0] in publisher or JUNK[0][1] in publisher or JUNK[0][2]:
                    publisher = publisher.replace(JUNK[0][0], '').replace(JUNK[0][1], '').replace(JUNK[0][2], '')

                year = '****'
                jornal = '****'


            data['Book'] = book
            data['Authors'] = authors
            data['Jornal'] = jornal
            data['Year'] = year
            data['Publisher'] = publisher

            link = item.find('a', href=True)
            if link:
                data['Link'] = link['href']
            else:
                data['Link'] = '****'

            datalist.append(data.copy())
            data.clear()


    except KeyboardInterrupt:
        print('Interrompendo requisição devido a interrupção forçada!\n')
        print(f'Error: {KeyboardInterrupt}')
        

    except IndexError:
        pass

    ingestocsv(datalist)


def scraping():
    try:
        url = requests.get(
            'https://scholar.google.com/scholar?start=130&q=gest%C3%A3o+da+diversidade&hl=en&as_sdt=0,5&as_vis=1').content

        soup = BeautifulSoup(url, 'html.parser')
        lista = soup.find_all('div', class_='gs_ri')
        filtering(lista)

    except ConnectionError:
        print(f'Ocorreu um erro de conexão, por favor verifique sua conexão com a internet!')
        print(f'Error: {ConnectionError}')


def ingestocsv(dados):
    with open('newdataframe.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)

        if os.stat('newdataframe.csv').st_size <= 0:
            writer.writeheader()

        writer.writerows(dados)


if __name__ == '__main__':
    scraping()
