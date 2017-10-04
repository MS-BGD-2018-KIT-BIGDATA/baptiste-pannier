#!/usr/local/bin/python3
import requests
from bs4 import BeautifulSoup


def str_to_int(s):
    s = s.replace(u'\xa0', u' ')
    s = s.replace(' ', '')
    return int(s)


def get_first_column(soup, search_term):
    # Get lines from the tables
    ss = soup.select("tr")
    # Get the lines containing the search term
    # (to get the corresponding column)
    elm = [s for i, s in enumerate(
        ss) if search_term in s.get_text()]
    # Since we're only interted by the first table :
    l = elm[0].get_text().split("\n")
    # Select the column
    col = [i for i, s in enumerate(
        l) if search_term in s]
    # We want the first column name "s"
    return col[0]


def get_line_first_column(soup, search_term):
    ss = soup.find_all(class_="bleu")
    l = ["= A", "= B", "= C", "= D"]
    res = []
    for p in l:
        line = [s for i, s in enumerate(
            ss) if p in s.get_text()]
        col = line[0].get_text().split("\n")
        s = str_to_int(col[get_first_column(soup, search_term)])
        res.append((p[-1] + "=", s))
    return res


prefix = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="
col = ["Euros par habitant", "Moyenne de la strate"]

for year in range(2010, 2016):
    url = prefix + str(year)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    for query in col:
        res = get_line_first_column(soup, query)
        print(query + ":", year, res)
