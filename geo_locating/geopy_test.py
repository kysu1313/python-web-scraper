#This project is solely used for educational purposes
#I decided to mess around and try out beautiful soup.
#this is what I came up with in about 2-ish hours 
#so I know its not pretty, but it does work.
#feel free to improve it. 

from bs4 import *
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from geopy.geocoders import Nominatim
import pickle as pl

#return the page html so you can pull data from it
def get_page_html(url):
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    return page_soup, page_html

#return the name of the shop or business
def get_name(container, counter):
    shop_name = container.find('a', class_="business-name").span
    shop_name = str(shop_name).split(">")
    #shop_name = str(shop_name).split("<")
    if counter > 0:
        shop_name = shop_name[1]
        shop_name = shop_name.split("<")[0]
    else:
        shop_name = "Add"
    return shop_name

#return the store address
def get_address(container, counter):
    full_address = ""
    if counter > 0:
        addr_container = container.find('p', class_="adr")
        street_addr = addr_container.span.text
        location_addr = addr_container.span.next_sibling.text
        location_addr = location_addr.split(",")[0]
        state_addr = addr_container.span.next_sibling.next_sibling.text
        # zip_addr = addr_container.span.next_sibling.next_sibling.next_sibling.text
        full_address = street_addr + " " + location_addr + " " + state_addr
        counter += 1
    else:
        full_address = " empty "
        counter += 1
    # print(full_address, "\n")
    return full_address

#get the store phone number
def get_phone(container, counter):
    number = 0
    if counter > 0:
        num_container = container.find('div', class_="phones phone primary").text
        number = num_container
        return number
    else:
        pass
    return number

#get the item number in the order they show up on the page
def get_item_number(container, counter):
    it_num = 0
    if counter > 0:
        it_num = container.find('h2', class_="n").text
    return it_num

#get the url of the next-page button at the botton of the page
def get_next_url(page_html, page):
    url_container = page_html.find('div', class_="pagination")
    #print(url_container)
    new_url = url_container.a['href']
    url = "https://www.yellowpages.com/search?search_terms=Coffee+Shops&geo_location_terms=Los%20Angeles%2C%20CA&page="+str(page)
    print(url)
    return url

def get_long_lat(addr):
    geolocator = Nominatim(user_agent="coffee_shops", timeout=3)
    location = geolocator.geocode(addr)
    if location:
        long = location.longitude
        lat = location.latitude
        return long, lat
    else:
        return 0, 0

def write_location_file(lat, long):
    f = open("test.txt", "a")
    f.write(str(lat) + "," + str(long) + "\n")
    print("Writing to file")
    f.close()

def write_address_file(addr):
    a = open("address.txt", "a")
    a.write(address + "\n")
    print("Writing to file")
    a.close()

location_dict = {'long':'lat'}


#loop through 7 pages. Didn't want to pull too many pages, 
#not sure how much strain this puts on their server
for page in range(1,9):

    #skip custom url for the first page
    if page == 1:
       url = "https://www.yellowpages.com/search?search_terms=Coffee+Shops&geo_location_terms=Los+Angeles%2C+CA"
    else:
        #start incrementing the page number and adding it to the end of the url
        url = "https://www.yellowpages.com/search?search_terms=Coffee+Shops&geo_location_terms=Los%20Angeles%2C%20CA&page="+str(page)

    p_soup = get_page_html(url)[0]
    #extract each store container on the page.
    #most store-like sites have easily iterable containers
    containers = p_soup.find_all('div', class_="info")
    counter = 0
    for container in containers:
        #return the actual store data
        item = str(get_item_number(container, counter))
        name = str(get_name(container, counter))
        address = str(get_address(container, counter))
        phone = str(get_phone(container, counter))

        longitude = get_long_lat(address)[0]
        latitude = get_long_lat(address)[1]
        #write_location_file(latitude, longitude)

        write_address_file(address)
        
        #format the output to the screen.
        #I know this is super messy, but it works and I'm lazy
        print("{:10} {:40} \n{:10} {:40} \n{:10} {:40} \n{:10} {:40} \n".format('Item: ', item, 'Name: ', name, 'Address: ', address, 'Phone: ', phone))
        counter += 1
    
    #increase the page to "click" the next page button
    page += 1
    print("Page: ", page)
    get_page_html(get_next_url(p_soup, page))

