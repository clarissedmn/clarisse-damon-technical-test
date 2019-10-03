import json
from datetime import datetime

def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

dict_output = {'rentals': []}

with open('data/input.json') as json_input:
    dict_input = json.load(json_input)
    for rental in dict_input['rentals']:
        diff_date = (datetime.strptime(
            rental['end_date'], '%Y-%m-%d') - datetime.strptime(rental['start_date'], '%Y-%m-%d')).days + 1
        rented_car_index = find(dict_input['cars'], "id", rental['car_id'])
        rented_car = dict_input['cars'][rented_car_index]
        dict_output['rentals'].append({
            "id": rental['id'],
            "price": (rental['distance'] * rented_car['price_per_km']) + (diff_date * rented_car['price_per_day'])
        })

with open('data/output.json', 'w') as outfile:
    json.dump(dict_output, outfile)
