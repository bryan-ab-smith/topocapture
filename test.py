import json
from typing import final

import requests

root_url = 'https://bryanabsmith.com/topomapper/datafiles/'
data_files = [
    'atsi',
    'business',
    'etc',
    'euexpl',
    'local',
    'monarchy',
    'none',
    'pol',
    'religious',
    'transplants',
    'war'
]

odonyms = {}

for theme in data_files:
    print(f'Adding {theme}')
    contents = requests.get(f'{root_url}{theme}.json')
    to_parse = contents.json()
    for odonym in to_parse['features']:
        # print(to_parse['features']['properties']['name'])
        odonyms[odonym['properties']['name']] = odonym['properties']['description'], odonym['properties']['refs']

print('Removing duplicates...')

final_odonyms = {}
for key, value in odonyms.items():
    if value not in final_odonyms:
        final_odonyms[key] = value

print(final_odonyms['Yarrawonga Drive'][1])
