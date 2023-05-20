import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

url = input('Link: ')

response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

pagination_links = soup.select('ul.pagination a[href]')

url_list = [url]
for link in pagination_links:
    href = link.get('href')
    if href not in url_list:
        url_list.append(href)

product_list = []
for url in tqdm(url_list):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    products = soup.find_all('div', class_='product-item-container')
    
    for values in products:
        name = values.find('h4').text.strip()
        price = values.find('span', class_='price-new').text.strip()
        
        product = {'Name': name, 'Price': price}
        product_list.append(product)

df = pd.DataFrame(product_list)
df.to_csv('product_data.csv', index=False)