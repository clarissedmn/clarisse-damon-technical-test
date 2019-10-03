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
        price = rental['distance'] * rented_car['price_per_km']

        for i in range(1, diff_date + 1):
            if i > 1 and i <= 4:
                price +=  0.9 * rented_car['price_per_day'] 
            elif i > 4 and i <= 10:
                price += 0.7 * rented_car['price_per_day'] 
            elif i > 10:
                price += 0.5 * rented_car['price_per_day']  
            else: 
                price += rented_car['price_per_day']
        
        fees = 0.3 * price
        insurance_fee = fees / 2
        assistance_fee = diff_date * 100
        drivy_fee = fees - insurance_fee - assistance_fee
                
        dict_output['rentals'].append({
            "id": rental['id'],
            "price": int(price),
            "commission": {
                "insurance_fee": int(insurance_fee),
                "assistance_fee": int(assistance_fee),
                "drivy_fee": int(drivy_fee)
            }
        })

with open('data/output.json', 'w') as outfile:
    json.dump(dict_output, outfile)

