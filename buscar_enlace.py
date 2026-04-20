import requests
from bs4 import BeautifulSoup

url = 'https://www.aprende.network/ligas.html'

respuesta = requests.get(url)

sopa = BeautifulSoup(respuesta.content, 'html.parser')

enlaces = sopa.find_all('a')

for enlace in enlaces:
    print(enlace.get('href'))
