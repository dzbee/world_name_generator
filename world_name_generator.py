import itertools
import requests
from requests_futures.sessions import FuturesSession
from bs4 import BeautifulSoup

NAME_URL = 'http://www.atlantagamer.org/iGM/RandomNames/index.php'

def gen_names(n_workers=4):
    template = BeautifulSoup(requests.get(NAME_URL).text, 'lxml')
    regions = [option['value'] for option in template.select('input[name="Languages"]')]
    genders = [option['value'] for option in template.select('input[name="Gender"]')]

    all_names = []
    session = FuturesSession(max_workers=n_workers)
    futures = [(session.post(NAME_URL, data={'generate': 'Generate',
                                            'Gender': gender,
                                             'Languages': region}),
                gender, region)
               for gender, region in itertools.product(genders, regions)]

    for future, gender, region in futures:
        names = list(BeautifulSoup(future.result().text, 'lxml').select('div#mainContent')[0].stripped_strings)
        all_names.extend(zip(names, [gender] * len(names), [region] * len(names)))

    return all_names
