#!/usr/local/bin/python3
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


class Vehicule:
    version = None
    km = None
    price = None
    phone = None
    seller = None
    url = None
    region = None
    location = None
    argus = None


def get_vehicule_price(soup):
    reg = "[0-9]+ [0-9]+.€"
    res = soup.find_all('h2', class_="item_price clearfix")
    r = re.search(reg, res[0].text)
    return int(r.group(0)[:-2].replace(" ", ""))


def get_vehicule_year(soup):
    reg = "[0-9]{4}"
    res = soup.find_all('span', itemprop="releaseDate")
    r = re.search(reg, res[0].text)
    return int(r.group(0))


def get_vehicule_km(soup):

    reg = "(.*?) KM"
    res = soup.find_all('h2', class_="clearfix")
    r = re.search(reg, res[5].text)
    km = r.group(0).replace(" ", "")
    km = km.replace("KM", "")
    return int(km)


def get_version(string):
    if re.search('intens', string, re.IGNORECASE):
        return "INTENS"
    elif re.search('zen', string, re.IGNORECASE):
        return "ZEN"
    elif re.search('life', string, re.IGNORECASE):
        return "LIFE"
    else:
        return None


def get_vehicule_version_from_desc(soup):
    res = soup.find_all('p', itemprop="description")
    return get_version(res[0].text)


def get_vehicule_version(soup):
    res = soup.find_all('h1', class_="no-border")
    v = get_version(res[0].text)

    if v is not None:
        return v
    else:
        return get_vehicule_version_from_desc(soup)


def get_pro_or_not(soup):
    res = soup.find_all('span', class_="ispro")
    if res:
        return "Pro"
    else:
        return "Part"


def get_vehicule_phone(soup):
    reg = "(0|\\+33|0033)[1-9][0-9]{8}"
    res = soup.find_all('p', itemprop="description")
    r = re.search(reg, res[0].text)
    if r:
        return r.group(0)
    else:
        return None


def get_vehicule_all_url_list(url_pages):
    url_list = []
    for url in url_pages:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        location = get_vehicule_location(url)
        url_list.extend(get_vehicule_url_list(soup, location))
    return url_list


def get_vehicule_location(url_pages):
    if re.search('ile_de_france', url_pages):
        return "ileDeFrance"
    elif re.search('aquitaine', url_pages):
        return "aquitaine"
    elif re.search('provence_alpes_cote_d_azur', url_pages):
        return "paca"
    else:
        return None


def get_vehicule_argus(version, year):
    intens = "https://www.lacentrale.fr/cote-auto-renault-zoe-intens+charge+rapide-"
    zen = "https://www.lacentrale.fr/cote-auto-renault-zoe-zen+charge+rapide-"
    life = "https://www.lacentrale.fr/cote-auto-renault-zoe-life+charge+rapide-"
    if version == "INTENS":
        url = intens + str(year) + ".html"
    elif version == "ZEN":
        url = zen + str(year) + ".html"
    elif version == "LIFE":
        url = life + str(year) + ".html"
    else:
        return None

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    res = soup.find_all('span', class_="jsRefinedQuot")
    return int(res[0].text.replace(" ", ""))


def get_vehicule_url_list(soup, location):
    urls = soup.find_all('a', class_="list_item clearfix trackable", href=True)
    url_list = list(map(lambda x: "https://" +
                        str(x['href'])[2:] + " " + location, urls))
    return url_list


def get_number_page(soup):
    page = soup.find_all('a', class_="element page")
    return len(page) + 1


def replace_page_number(string, n):
    return re.sub('[0-1]', str(n), string)


def get_page(npage, url):
    l = [replace_page_number(url, n) for n in range(1, npage + 1)]
    return l


def gen_seed(l):
    head_url = "https://www.leboncoin.fr/voitures/offres/"
    mid_url = "/?o=1"
    tail_url = "&q=zoe"

    return [head_url + i + mid_url + tail_url for i in l]


def put_in_df(Vehicules):
    df = pd.DataFrame(columns=['region', 'version', 'year', 'km',
                               'price', 'argus', 'seller', 'phone', 'url'])
    for i in Vehicules:
        df.loc[-1] = [str(i.location), str(i.version), int(i.year),
                      int(i.km), int(i.price), i.argus,
                      str(i.seller), str(i.phone), str(i.url)]
        df.index = df.index + 1

    df[['year', 'km', 'price']] = df[[
        'year', 'km', 'price']].astype(int)
    df[['region', 'version', 'seller', 'phone', 'url']] = df[[
        'region', 'version', 'seller', 'phone', 'url']].astype(str)
    return df


def get_vehicule_properties(url):
    url, location = url.split(" ")
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    vehicule = Vehicule()
    vehicule.url = url
    vehicule.location = location
    vehicule.price = get_vehicule_price(soup)
    vehicule.year = get_vehicule_year(soup)
    vehicule.km = get_vehicule_km(soup)
    vehicule.version = get_vehicule_version(soup)
    vehicule.seller = get_pro_or_not(soup)
    vehicule.phone = get_vehicule_phone(soup)
    vehicule.argus = get_vehicule_argus(vehicule.version, vehicule.year)

    return vehicule


region = ['ile_de_france', 'aquitaine', 'provence_alpes_cote_d_azur']
gen_seed(region)

url_pages = []
url_seed = gen_seed(region)

for i in url_seed:
    r = requests.get(i)
    soup = BeautifulSoup(r.text, 'html.parser')
    npage = get_number_page(soup)
    url_pages.extend(get_page(npage, i))


url_list = get_vehicule_all_url_list(url_pages)

Vehicules = list(map(lambda x: get_vehicule_properties(x), url_list))

df = put_in_df(Vehicules)

df.to_csv("output.csv")
