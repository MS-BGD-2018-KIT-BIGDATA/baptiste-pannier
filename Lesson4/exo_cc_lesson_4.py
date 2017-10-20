import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import simplejson
import urllib


class Medic:
    titulaire = None
    date = None
    price = None
    restric = None


url = "https://www.open-medicaments.fr/api/v1/medicaments?query=ibuprof%C3%A8ne"

r = simplejson.load(urllib.request.urlopen(url))
id_med = [i['codeCIS'] for i in r]

url2 = "https://www.open-medicaments.fr/api/v1/medicaments/"

for i in id_med:
    url = url2 + i
    r = simplejson.load(urllib.request.urlopen(url))
    titulaire = r['titulaires']
    date = r['dateAMM']
    if 'prix' in r:
        price = r['prix']
    else:
        price = None
    restric = r['indicationsTherapeutiques']
    print(titulaire, date, price)
