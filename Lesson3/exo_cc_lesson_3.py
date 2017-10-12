#!/usr/local/bin/python3
import sys
import requests
from bs4 import BeautifulSoup
import pprint
import simplejson
import urllib
from collections import defaultdict


# GET name
url = "https://lespoir.jimdo.com/2015/03/05/classement-des-plus-grandes-villes-de-france-source-insee/"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
res = soup.tbody.find_all("tr")
city_list = list(map(lambda x: x.text.split()[1], res))

mykey = "mytoken"

# Distance
d = defaultdict(list)
for i in city_list[1:5]:
    for j in city_list[1:5]:
        if i != j:
            url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + \
                i + "&destinations=" + j + "&key=" + mykey
            result = simplejson.load(urllib.request.urlopen(url))
            # (In minutes)
            driving_time = result['rows'][0]['elements'][0]['duration']['value'] / 60.
            d[i].append((j, driving_time))


pp = pprint.PrettyPrinter(indent=2)
pp.pprint(d)
