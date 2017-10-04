#!/usr/local/bin/python3
import requests
from bs4 import BeautifulSoup


part1 = "https://www.cdiscount.com/search/10/"
part2 = ".html#_his_"


def get_old_price(old_price):
    l = []

    for i in old_price:
        a = i.get_text()
        l.append(a)
    return l


def get_promo(promo):
    l = []
    for i in promo:
        a = i.get_text()
        myList = a.split(" ")
        l.append(myList[1])

    return l


for elm in ["acer", "dell"]:
    url = part1 + elm + part2

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    new_price = soup.find_all(class_="price")
    old_price = soup.find_all(class_="prdtPrSt")
    promo = soup.find_all(class_="ecoBlk")

    l = get_old_price(old_price)
    l2 = get_promo(promo)
    print(elm)
    print(l)
    print(l2)

    # Reste à comparer l et l2...
    # pour obtenir un pourcentage moyen
    # faire attention aux reduction en euros et en %
    # et surtout, gérer les éléments vides
    # puis comparer acer et dell
