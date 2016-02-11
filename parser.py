import sys, itertools, json

def get_data():
    data = {}
    contents = map(int, open(sys.argv[1]).read().replace("\n", ' '). split())
    data['rows'] = contents.pop(0)
    data['columns'] = contents.pop(0)
    data['drones'] = contents.pop(0)
    data['turns'] = contents.pop(0)
    data['max_payload'] = contents.pop(0)

    data['products'] = {}
    data['products']['number'] = contents.pop(0)
    data['products']['weights'] = []

    for i in range(0, data['products']['number']):
        data['products']['weights'].append(contents.pop(0))


    data['warehouses'] = {}
    data['warehouses']['number'] = contents.pop(0)
    data['warehouses']['informations'] = [ None ] * data['warehouses']['number']
    for i in range(0, data['warehouses']['number']):
        data['warehouses']['informations'][i] = {}
        data['warehouses']['informations'][i]['location'] = {
            'x': contents.pop(0),
            'y': contents.pop(0)
        }
        data['warehouses']['informations'][i]['products'] = []
        for j in range(0, data['products']['number']):
            data['warehouses']['informations'][i]['products'].append(contents.pop(0))

    data['orders'] = {}
    data['orders']['number'] = contents.pop(0)
    data['orders']['informations'] = [ None ] * data['orders']['number']
    for i in range(0, data['orders']['number']):
        data['orders']['informations'][i] = {}
        data['orders']['informations'][i]['location'] = {
            'x': contents.pop(0),
            'y': contents.pop(0)
        }
        data['orders']['informations'][i]['items'] = {}
        data['orders']['informations'][i]['items']['number'] = contents.pop(0)
        data['orders']['informations'][i]['items']['products'] = []
        for j in range(0, data['orders']['informations'][i]['items']['number']):
            data['orders']['informations'][i]['items']['products'].append(contents.pop(0))
    return data
