
import requests   
  
def data_wragling():
 url = requests.get('https://api.nasa.gov/planetary/apod?api_key=uADUDTja167n6W8yzg03xI1DWnmVkndjbviN0a2t').json()
print(url)

def main():
 data_wragling()

  
if __name__ == '__main__':
 main()
