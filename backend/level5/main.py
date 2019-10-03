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
        
        total_fees = 0.3 * price
        insurance_fee = total_fees / 2
        assistance_fee = diff_date * 100
        
        rental_options = []
        driver_debit = price
        owner_credit = price - total_fees
        drivy_credit = total_fees - insurance_fee - assistance_fee

        for option in dict_input['options']:
            if option['rental_id'] == rental['id']:
                current_option = option['type']
                rental_options.append(current_option)
                if current_option == 'gps':
                    option_price = 500 * diff_date 
                    driver_debit += option_price
                    owner_credit += option_price
                elif current_option == 'baby_seat':
                    option_price = 200 * diff_date 
                    driver_debit +=  option_price
                    owner_credit += option_price
                else:
                    option_price = 1000 * diff_date 
                    driver_debit += option_price
                    drivy_credit += option_price

        dict_output['rentals'].append({
            "id": rental['id'],
            "options": rental_options,
            "actions": [
                {
                    "who": "driver",
                    "type": "debit",
                    "amount": int(driver_debit)
                },
                {
                    "who": "owner",
                    "type": "credit",
                    "amount": int(owner_credit)
                },
                {
                    "who": "insurance",
                    "type": "credit",
                    "amount": int(insurance_fee)
                },
                {
                    "who": "assistance",
                    "type": "credit",
                    "amount": int(assistance_fee)
                },
                {
                    "who": "drivy",
                    "type": "credit",
                    "amount": int(drivy_credit)
                }
            ]
        })

with open('data/output.json', 'w') as outfile:
    json.dump(dict_output, outfile)
