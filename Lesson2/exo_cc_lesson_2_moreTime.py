#!/usr/local/bin/python3
import requests
from bs4 import BeautifulSoup


part1 = "https://www.cdiscount.com/search/10/"
part2 = ".html#_his_"


def get_old_price(old_price):
    l = []

    for i in old_price:
        a = i.get_text()
        if a != '':
            l.append(a)
    return l


def get_promo(promo):
    l = []
    for i in promo:
        a = i.get_text()
        myList = a.split(" ")
        l.append(myList[1])

    return l


def clean_data(i):
    t = i.replace("€", "")
    l = t.split(",")
    return int(l[0])


def compare(op, promo):
    res = []

    for i in range(len(promo)):
        if "%" in promo[i]:
            t = promo[i].replace("%", "")
            t = (int(t) / 100) * clean_data(op[i])
            promo[i] = int(t)

    # clean promo
    for i in promo:
        if(isinstance(i, str)):
            t = i.replace("€", "")
            res.append(int(t))

    res2 = []
    # # clean op
    for i in op:
        t = i.split(",")
        res2.append(int(t[0]))

    k = [(x / (x + y)) * 100 for x, y in zip(res, res2)]
    return k


def mean(l):
    return sum(l) / len(l)


for elm in ["acer", "dell"]:
    url = part1 + elm + part2

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    new_price = soup.find_all(class_="price")
    old_price = soup.find_all(class_="prdtPrSt")
    promo = soup.find_all(class_="ecoBlk")

    l = get_old_price(old_price)
    l2 = get_promo(promo)

    res = compare(l, l2)
    print(elm + ": Mean (%)")
    print(mean(res))
