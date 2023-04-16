
# Importação das bibliotecas necessárias para o funcionamento do 'web' scraper
import csv
import os
import requests
from bs4 import BeautifulSoup
from minimalyear import etl_process

# Constantes da aplicação
# Constante utilizadas para a remoção de informações desnecessárias após a coleta dos dados do Google Scholar
FIELDS = ['Book', 'Authors', 'Jornal', 'Year', 'Publisher', 'Link']
JUNK = [['… ', ' ', ' …', ' ', '…'], ['[HTML]', '[PDF]', '[LIVRO][B]', '[BOOK][B]', '[CITATION][C]']]

# Variáveis usadas para a coleta dos dados
datalist = []  # Lista utilizada para salvar os dicionários apos a coleta dos dados
data = {}  # Dicionario para salvar temporariamente os dados do artigo/ livro


# Função utilizada para remover as informações desnecessárias e após a remoção salvar os dados em um dicionário de dados
def filtering(lista):
    try:

        # Itera sobre a lista de resultados da pesquisa passada como parâmetro da função
        for item in lista:

            # Salva o nome do artigo/livro, e remove informações desnecessárias
            book = item.find('h3', class_='gs_rt').text.strip()
            for junk in JUNK[1]:
                book = book.replace(junk, '')

            # Verifica o tamanho da 'string' após realização de quebra do texto pelo elemento hífen Sendo o tamanho
            # da variável maior ou igual a 3, coleta dados de autores, jornal, publicadora e ano,
            # e remove informações desnecessárias
            item_length = item.find('div', class_='gs_a').text.split('-')
            if len(item_length) >= 3:

                authors = item.find('div', class_='gs_a').text.strip().split('-')[0]
                for junk in JUNK[0]:
                    authors = authors.replace(junk, ' ')

                jornal = item.find("div", class_="gs_a").text.strip().split('-')[1].strip().split(',')[0]
                for junk in JUNK[0]:
                    jornal = jornal.replace(junk, ' ')

                year = item.find("div", class_='gs_a').text.strip().split('-')[1].split()[-1]

                publisher = item.find("div", class_="gs_a").text.strip().split('-')[2].strip()
                for junk in JUNK[0]:
                    publisher = publisher.replace(junk, ' ')

            # No caso do tamanho da variável ser menor que três, apenas a coleta de dados do artigo e autores é
            # realizada '****' é atribuído às variáveis de 'journal' e 'year', tendo em vista o padrão do Google
            # Scholar.
            else:

                authors = item.find('div', class_='gs_a').text.strip().split('-')[0]
                for junk in JUNK[0]:
                    authors = authors.replace(junk, ' ')

                publisher = item.find("div", class_="gs_a").text.strip().split('-')[-1].strip()
                for junk in JUNK[0]:
                    publisher = publisher.replace(junk, ' ')

                year = '****'
                jornal = '****'

            # Insere os dados coletados temporariamente no dicionário de dados.
            data['Book'] = book
            data['Authors'] = authors
            data['Jornal'] = jornal
            data['Year'] = year
            data['Publisher'] = publisher

            # salva o link do artigo, caso ele tenha um link
            link = item.find('a', href=True)
            if link:
                data['Link'] = link['href']
            else:
                data['Link'] = '****'

            # Salva o dicionário em uma lista e limpa o dicionário para uma nova coleta
            datalist.append(data.copy())
            data.clear()

    # Caso haja a interrupção da aplicação pelo usuário, uma mensagem de erro é retornada
    except KeyboardInterrupt:
        print('Interrompendo requisição devido à interrupção forçada!\n')
        print(f'Error: {KeyboardInterrupt}')


    for x in enumerate(datalist):
        for k, v in x[1].items():
            if k == 'Jornal' and v.isnumeric():
                x[1]['Jornal'] = '****'
                x[1]['Year'] = v
            
            if k == 'Year' and v.isnumeric() == False:
                x[1]['Year'] = '****'
                x[1]['Jornal'] = v

    # Após a iteração sobre a lista, chama a função ingestão de dados passando como o parâmetro a lista que guarda os
    # dicionários de dados
    ingestocsv(datalist)


# Função de ingestão de dados em arquivo CSV
def ingestocsv(dados):
    if os.path.exists('rawdata\\dadosraiz.csv'):
        os.remove('rawdata\\dadosraiz.csv')

    with open('rawdata\\dadosraiz.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(dados)


def main():
    # Variável de controle do laço de repetição do programa
    c = 1

    subject = str(input('Digite o assunto do artigo que deseja recuperar: '))
    quantity = str(input('Digite quantas paginas de artigos que deseja recuperar: '))

    for x in range(0, int(quantity) * 10, 10):

        # Tenta fazer a requisição ao link desejado
        try:
            url = requests.get(
                f'https://scholar.google.com/scholar?start={x}&q={subject}&hl=en&as_sdt=0,5').content

            # Salva o campo HTML desejado de toda a página para uma lista e chama a função de coleta e limpeza de dados
            soup = BeautifulSoup(url, 'html.parser')
            lista = soup.find_all('div', class_='gs_ri')
            filtering(lista)

        # Caso o usuário não esteja conectado com a 'internet' a aplicação é interrompida, e uma mensagem de erro é exibida
        except requests.exceptions.RequestException:
            print(f'Ocorreu um erro de conexão, por favor verifique sua conexão com a internet!')
            print(f'Erro: {requests.exceptions.RequestException}')

        except ValueError as error:
            print(f'Ocorreu um erro ao tentar coletar quantas paginas voce deseja recuperar\n')
            print(f'Error: {error}')

        finally:
            print(f'Pagina {c} coletada com sucesso!')
            c += 1    

    etl_process()

# Inicializa da aplicação
if __name__ == '__main__':
    main()
