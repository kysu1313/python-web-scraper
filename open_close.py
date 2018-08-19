import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from datetime import datetime
import pandas as pd
import csv


with open("Intel Motherboards.csv") as f:
    reader = csv.reader(f)
    for item in range(1, 10):
        print(next(reader)[item])
    print(reader[1])

# csvfile = open('intelmb.csv', 'r')

df = pd.read_csv("Intel Motherboards.csv", skiprows=[25, 125])

print(df.head())
print(df)
rows = len(df)
for row in range(1,rows):
    print(df.row(row))
