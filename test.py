import json

with open('atsi.json') as f:
    vals = json.load(f)
    for x in vals['features']:
        print(x['properties']['name'], ':', x['properties']['description'])
    # print(vals['features'][0]['properties']['name'])
    # for x in vals:
        # print(x['features'])