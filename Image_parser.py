import requests
from tqdm import tqdm
import os
from bs4 import BeautifulSoup
import urllib3

lib = urllib3.PoolManager()

def get_item_url(img):
    links_list = []
    for items in img:
        item_url = items.get('src')
        links_list.append(item_url)
    return links_list

def image_parser(query):

    HTTP_response = lib.request('GET', query)
    data = HTTP_response.data
    soup = BeautifulSoup(data, 'lxml')
    img = soup.find_all('img')

    links_list = get_item_url(img)

    response = requests.get(query)

    img_dir_path = ''.join(query.split('.')[1])

    if not os.path.exists(img_dir_path):
        os.makedirs(img_dir_path)


    if response.status_code != 200:
        print(f'Error: {response.status_code}')

    donwload_imaged(links_list, img_dir_path)

def donwload_imaged(img_list, img_dir_path):
    for item_url in tqdm(img_list):
        response = requests.get(item_url)
        name = item_url.split('/')[-1]

        if response.status_code == 200:
            try:
                with open(f'{img_dir_path}/{name}', 'wb') as file:
                    print(item_url)
                    file.write(response.content)
                    file.close()
            except OSError as ex:
                print(f'{item_url} : {ex}')
                pass
        else:
            print(f'This link is unavaible: {item_url}')
            pass

def main():
    query = input('Enter page link: ')
    image_parser(query=query)

if __name__ == '__main__':
    main()
