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


def get_medic_properties(medic_id):

    url = "https://www.open-medicaments.fr/api/v1/medicaments/" + medic_id

    r = simplejson.load(urllib.request.urlopen(url))
    medic = Medic()
    medic.titulaire = r['titulaires']
    medic.date = r['dateAMM']
    if 'prix' in r:
        medic.price = r['prix']
    else:
        medic.price = None
    restric = r['indicationsTherapeutiques']
    r = re.search("[0-9]+ kg", restric)
    if r is not None:
        medic.restric = r.group(0)[0:-3]
    else:
        medic.restric = None

    return medic


url = "https://www.open-medicaments.fr/api/v1/medicaments?query=ibuprof%C3%A8ne"
r = simplejson.load(urllib.request.urlopen(url))
id_med = [i['codeCIS'] for i in r]

medics = list(map(lambda x: get_medic_properties(x), id_med))

print(medics[0].titulaire)
print(medics[0].price)
print(medics[0].date)
print(medics[0].restric)
