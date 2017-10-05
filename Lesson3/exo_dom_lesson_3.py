#!/usr/local/bin/python3
import sys
import requests
from bs4 import BeautifulSoup
import pprint
import getpass


def mean(l):
    """
    Simply a mean function
    on a list of numbers
    """
    return float(sum(l)) / max(len(l), 1)


def get_stars(d: dict):
    """
    From a dictionnary composed of
    elements in a JSON, return the
    number of stargazers_count if
    the git repo is not a fork
    else return None
    """
    if not d["fork"]:
        return d["stargazers_count"]
    else:
        return None


def main(argv):
    user = input("Username on GitHub:")
    passwd = getpass.getpass("Password for " + user + " on GitHub:")

    # Get list of famous coders
    url = "https://gist.github.com/paulmillr/2657075"
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    res = soup.tbody.find_all("tr")

    name = list(map(lambda x: x.text.split(" ")[2], res))

    # Now let's get the mean number of stars
    # of all repositories for all name
    result = dict()
    for i in name:
        r = requests.get('https://api.github.com/users/'
                         + i + '/repos?per_page=1000',
                         auth=(user, passwd))
        d = r.json()
        l = list(filter(None.__ne__, map(lambda x: get_stars(x), d)))
        result[i] = mean(l)

    result = [(k, result[k])
              for k in sorted(result, key=result.get, reverse=True)]
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(result)

    pass


if __name__ == "__main__":
    main(sys.argv)
