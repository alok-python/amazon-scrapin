import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import pandas as pd


def get_product_data(url):
    url=url
    payload = {}
    headers = {
        'device-memory': '8',
        'sec-ch-device-memory': '8',
        'dpr': '1.1',
        'sec-ch-dpr': '1.1',
        'viewport-width': '1682',
        'sec-ch-viewport-width': '1682',
        'rtt': '50',
        'downlink': '10',
        'ect': '4g',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-ch-ua-platform-version': '"6.2.0"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'host': 'www.amazon.in'
        }
    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        raw_html = response.text
        product_soup = BeautifulSoup(raw_html, features="html.parser")
        return product_soup
    

def get_review_data(asin_code:str):

    url = f"https://www.amazon.in/review/widgets/average-customer-review/popover/ref=acr_search__popover?ie=UTF8&asin={asin_code}&ref=acr_search__popover&contextId=search"

    payload = {}
    headers = {
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-device-memory': '8',
        'sec-ch-viewport-width': '1920',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'X-Requested-With': 'XMLHttpRequest',
        'dpr': '1',
        'downlink': '10',
        'sec-ch-ua-platform': '"Windows"',
        'device-memory': '8',
        'rtt': '0',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'viewport-width': '1920',
        'Accept': 'text/html,*/*',
        'sec-ch-dpr': '1',
        'ect': '4g',
        'host': 'www.amazon.in',
        'Cookie': 'session-id=260-8935756-1783025; session-id-time=2082787201l'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        raw_html = response.text
        review_soup = BeautifulSoup(raw_html, features="html.parser")
        return review_soup

def get_amazon_request_data(page_no: int):
    url = f"https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba,aps,283&ref=sr_pg_{page_no}"

    payload = {}
    headers = {
  'device-memory': '8',
  'sec-ch-device-memory': '8',
  'dpr': '1.1',
  'sec-ch-dpr': '1.1',
  'viewport-width': '1682',
  'sec-ch-viewport-width': '1682',
  'rtt': '50',
  'downlink': '10',
  'ect': '4g',
  'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"',
  'sec-ch-ua-platform-version': '"6.2.0"',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'host': 'www.amazon.in'
}

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.text


product_data = []
for i in range(1,5):
    raw_html = get_amazon_request_data(page_no=i)
    soup = BeautifulSoup(raw_html, features="html.parser")
    all_seach_items = soup.find_all(attrs={"data-component-type": "s-search-result"})
    for search_item in all_seach_items:
        prod_asin = search_item['data-asin']
        product_title = search_item.find(attrs={"class": "a-size-medium a-color-base a-text-normal"})
        product_link_data = search_item.find(attrs={"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
        product_link_str = urllib.parse.unquote(product_link_data['href'])
        product_link = product_link_str[product_link_str.find('url=') + len('url=') + 1: product_link_str.find('/ref=')]
        product_price = search_item.find(attrs={"class": "a-price-whole"})
        review_soup = get_review_data(asin_code=prod_asin)
        product_avg_rating = 0
        product_review_count = 0
        if review_soup:
            average_rating_str = review_soup.find(attrs={'data-hook' : "acr-average-stars-rating-text"})
            review_count_str = review_soup.find(attrs={'data-hook' : "total-review-count"})
            if average_rating_str:
                product_avg_rating = average_rating_str.text.split(" ")[0]
            if review_count_str:
                product_review_count = review_count_str.text.split(" ")[0]

        current_product = {
            'product_url': f"https://www.amazon.in/{product_link}",
            'product_name': product_title.text,
            'product_price': product_price.text,
            'rating': product_avg_rating,
            'number_of_reviews': product_review_count
        }
        product_data.append(current_product)

df = pd.DataFrame(product_data)

df.to_csv('product_listing.csv', index=False)





producrlisting = 'product_listing.csv'
df = pd.read_csv(producrlisting)
product_urls = df['product_url'].tolist()

product_details=[]
len=1
for i in product_urls:
   len=len+1
   if len==201:
       break
   else:
    product_soup=get_product_data(i)
    product_description=product_soup.find(id="productDescription")
    product_descriptions=''
    try:
        product_descriptions=product_description.text
    except:
        product_descriptions=""
    ASIN=i.split('/')[-1]
    description=product_soup.find(id="feature-bullets")
    try:
     product_manufacturer = product_soup.find(id="detailBullets_feature_div")
     list_items = product_manufacturer.find_all('li')
     manufacturer = ""
     for li in list_items:
         header_span = li.find('span', class_='a-text-bold')
         data_span = li.find('span', class_='a-list-item')
         if header_span and data_span:
             header_text = header_span.get_text(strip=True).lower()
             data_text = data_span.get_text(strip=True)
             if "manufacturer" in header_text:
                  manufacturer = data_text.split(':')[1].strip()


    except:
        product_ma = product_soup.find(id="productDetails_techSpec_section_1")
        rows = product_ma.find_all('tr')
        manufacturer = ""
        for row in rows:
            header = row.find('th', class_='a-color-secondary')
            data = row.find('td', class_='a-size-base prodDetAttrValue')
            if header and data:
                header_text = header.get_text(strip=True)
                data_text = data.get_text(strip=True)
                if header_text == "Manufacturer":
                    manufacturer = data_text
                   
       
   
   


   current_product = {
            'description': description.text,
            'asin': ASIN,
            'product_description': product_descriptions,
            'Manufacturer': manufacturer,
            
        }

   product_details.append(current_product)


df = pd.DataFrame(product_details)

df.to_csv('product_details.csv', index=False)


   

   

       
