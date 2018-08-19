import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from datetime import datetime
import pandas as pd
import numpy as np
import math
import csv


filename = "Intel_Motherboards.csv"
price_file = "price_list_new.csv"

d_full = pd.read_csv(filename, skiprows=[37])
d_prices = pd.read_csv(price_file, skiprows=[37])

print(d_full.head())
# print(d_prices.head())

#print(d_full.values.tolist())
# print(d_prices.values.tolist())

full_data_list = d_full.values.tolist()
price_list = d_prices.values.tolist()

print(full_data_list[1][6])
print(price_list[1][1])

price_list[5][2] = 500.00

if len(full_data_list) <= len(price_list):
    list_length = len(full_data_list)
elif len(full_data_list) >= len(price_list):
    list_length = len(price_list)

for x in range(list_length):
    new_price_id = full_data_list[x][1]
    old_price_id = price_list[x][1]
    item_name = full_data_list[x][3]
    if new_price_id == old_price_id:
        print(str(x) + " ID match")
        new_price = full_data_list[x][6]
        old_price = price_list[x][2]
        if new_price < old_price:
            print("Price drop: " + item_name)
