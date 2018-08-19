#!/usr/bin/env python3

import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from datetime import datetime
import pandas as pd
import numpy as np
import math
import csv


def get_general_product(url):
    page_html = get_page_html(url)
    page_soup = soup(page_html, "html.parser")
    title = page_soup.find('h1', class_="page-title-text")
    # print(title.text)
    return title.text

#return the actual product info
def get_info(container, row_number):
    item_id_string = container.a['href']
    item_id = item_id_string.split("=")[1]
    item_link = container.find('a', class_="item-title")['href']
    # print(item_link)
    brand = container.div.div.a.img["title"]
    title = container.a.img["alt"]
    price_container = container.find("li", class_="price-current")
    shipping_container = container.find("li", class_="price-ship")
    # isolate the score and total ratings
    rating_container = container.find("a", class_="item-rating")
    if container.has_attr("item-rating"):
        rating_score = rating_container['title']
        final_score = rating_score.split(" ")[2]
        total_ratings = rating_container.span.text
        total_ratings = total_ratings.split("(")[1]
        total_ratings = total_ratings.split(")")[0]
    else:
        rating_score = "0"
        final_score = "0"
        total_ratings = "0"

    # print(total_ratings)
    # print(final_score)
    if check_sold_out(container) == True:
        price = 0
    elif price_container.strong == None:
        price = 0
    else:
        price = price_container.strong.text
    ship_price = shipping_container.text.split()[0]
    ship_price_number = ship_price.split("$")
    shipping_cost = 0
    #determine if shipping is free or not
    if len(ship_price_number)<2:
        ship_price_number = 0
    else:
        shipping_cost = ship_price_number[1]
    total_price = float(price) + .99 + float(shipping_cost)
    return row_number, item_id, item_link, brand, title, price, shipping_cost, total_price, final_score, total_ratings

def write_file(file, row_number, item_id, item_link, brand, title, price, shipping_cost, total_price, final_score, total_ratings):
    #write the product info to a .csv file
    f.write(str(row_number) + "," + item_id + "," + item_link + "," + brand + "," + title + "," + str(price) + "," + str(shipping_cost) + "," + str(total_price) + "," + str(final_score) + "," + str(total_ratings) + "\n\n")
    

def write_price_file(file, row_number, item_id, total_price, total_ratings):
    p.write(str(row_number) + "," + str(item_id) + "," + str(total_price) + "," + str(total_ratings) + "\n")
    

def get_page_html(my_url):
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    return page_html

#get the html item containers
def get_containers(page_html):
    page_soup = soup(page_html, "html.parser")
    containers = page_soup.find_all('div', class_="item-container")
    return containers

def get_item_id(container):
    return container.a['href']

def get_item_cost(container):
    price_container = container.find("li", class_="price-current")
    price = 0
    if check_sold_out(container) == False:
        price = 9999
    else:
        price = price_container.strong.text
    return price

def get_item_name(container):
    title = container.a.img["alt"]
    return title

def check_sold_out(container):
    if container.has_attr("priceAction"):
        return True 
    else:
        return False

def print_item_details(row, id, link, brand, title, price, shipping, total, score, ratings):
    print("Row: " + str(row))
    print("ID: " + id)
    print("Link: " + link)
    print("Brand: " + brand)
    print("Title: " + title)
    print("Price: " + str(price))
    print("Shipping: " + str(shipping))
    print("Total: " + str(total))
    print("Score: " + str(score))
    print("Ratings: " + str(ratings) + "\n")

def compare_prices(file, old_price_list):
    with open(file, buffering=1000) as f:
        for row in f:
            row_counter += 1
            row = json.loads(row)
            parent_id = row['parent_id']
            body = format_data(row['body'])
            created_utc = row['created_utc']
            score = row['score']
            comment_id = row['id']
            subreddit = row['subreddit']

            parent_data = find_parent(parent_id)
        f.close()

filename = "Intel_Motherboards2.csv"
f = open(filename, "w+")
headers = "row, item_id, item_link, brand, product_name, price, shipping, total, score, total_ratings\n"
f.write(headers)

pricefile = "prices.csv"
p = open(pricefile, "w+")
headers = "row, item_id, total, total_ratings\n"
p.write(headers)

for page in range(1, 6):
    #organize by date
    timeframe = datetime.now()
    #array to store old prices
    old_prices = np.array(0)

    if page == 1:
        url = 'https://www.newegg.com/Intel-Motherboards/SubCategory/ID-280?order=BESTMATCH&PageSize=60'
    else:
        url = "https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48/Page-" + str(page) + "?Tid=7709&PageSize=36&order=BESTMATCH"
    # filename = str(get_general_product(url)) + ".csv"
    print("Page: " + str(page) + "\nurl: " + url)

    id = ""
    link = ""
    date = timeframe
    brand =""
    title = ""
    price = 0.0
    shipping = 0.0
    total = 0.0
    score = 0
    ratings = 0

    containers = get_containers(get_page_html(url))
    container_count = 0

    

    for container in containers:
        check_sold_out(container)
        # print(container_count)
        row, id, link, brand, title, price, shipping, total, score, ratings = get_info(container, container_count)
        write_file(filename, row, id, link, brand, title, price, shipping, total, score, ratings)
        print_item_details(row, id, link, brand, title, price, shipping, total, score, ratings)
        #uncomment to re-write prices to file
        #write_price_file(price_file, row, id, total, ratings)
        container_count += 1

p.write("Edited: " + str(timeframe))
p.close()
f.write("Edited: " + str(timeframe))
f.close()    
