import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from datetime import datetime

#organize by date
timeframe = datetime.now()

#create and open a .csv file called "products"
filename = "products.csv"
f = open(filename, "w")

my_url = 'https://www.newegg.com/Intel-Motherboards/SubCategory/ID-280?order=BESTMATCH&PageSize=96'
headers = "item_id, brand, product_name, price, shipping, total, score\n"
f.write(headers)
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")
containers = page_soup.find_all('div', class_="item-container")

title = page_soup.find('h1', class_="page-title-text")

for container in containers:
    item_action = container.find('div', class_="item-action")
    print(item_action)
    #print(item_action.div.div.span)
    # if container.find("li", class_="price-current") == None:
    #     print("ERROR")
    #     print(container.a.img["alt"])
    # else:
    #     price_container = container.find("li", class_="price-current")
    #     print(container.a.img["alt"])


print(title.text)























#s
