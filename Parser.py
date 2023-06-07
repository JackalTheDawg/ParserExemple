from bs4 import BeautifulSoup
import urllib3

lib = urllib3.PoolManager()

url = 'https://www.youtube.com/'
response = lib.request('GET', url)
data = response.data
soup = BeautifulSoup(data, 'lxml')

links = soup.find_all('a')

for items in links:
    item_text = items.text
    item_url = items.get('href')
    print(f'{item_text}: {item_url}')
