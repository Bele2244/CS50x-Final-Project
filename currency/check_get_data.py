from decimal import Decimal
from . models import Currency

# Symbol is valid return uppercase symbol 
def check_symbol(country_info, form_input):
    form_length = len(form_input)
    if form_length < 3:
        return None
    elif form_length == 3:
        form_input = form_input.upper()
        for row in country_info:
            if form_input == row['Code']:
                return row['Code']
    elif form_length != 3:
        form_input = form_input.title()
        for row in country_info:
            if form_input in row['Country']:
                return row['Code']
    return None
        
# Return the list of dictionaries of countries with matching symbol
def get_symbol_country(country_info, symbol):
    all_countries = []
    country = {}
    for row in country_info:
        if row['Code'] == symbol:
           all_countries.append(row['Country'])

    return sorted(all_countries)

# Returns symbol if found or conversion amount based on 1 usd 
def get_symbol_value(db_currency_items, currency_info, convert_amount=None, convert_symbol=None):

    if convert_amount:
        # Converting currency 1 usd equivalent
        convert_amount = Decimal(convert_amount)
        rate_found = 0
        for row in currency_info:
            if convert_symbol == row['Code']:
                convert_symbol_usd_rate = Decimal(row['Value'])
                rate_found = 1
                break 
        # Convert db currencies to desired amount 
        for row_db in db_currency_items:
            row_db['value'] = ''
            for row_curr in currency_info:
                if row_db['symbol'] == row_curr['Code']:
                    # Converting rate found - current currency to usd equivalent 
                    if rate_found:
                        to_usd = Decimal(row_curr['Value'])
                        # Convert currency based on 1 usd
                        converted_value = convert_currency(convert_amount, convert_symbol_usd_rate, to_usd)
                        row_db['value'] = f"{float(converted_value):,.2f}"

        # First symbol in the list
        first_symbol = db_currency_items[0]['symbol']
        first_symbol_value = db_currency_items[0]['value']

        for row in db_currency_items:
            if row['symbol'] == convert_symbol:
                # swap first symbol with converting symbol and place it on top
                second_symbol = row['symbol']
                second_symbol_value = row['value']

                db_currency_items[0]['symbol'] = row['symbol'] 
                db_currency_items[0]['value'] = row['value']

                row['symbol'] = first_symbol
                row['value'] = first_symbol_value
                
                break
    else:
        # Convert db currencies to desired amount 
        for row_db in db_currency_items:
            row_db['value'] = ''
            for row_curr in currency_info:
                if row_db['symbol'] == row_curr['Code']:
                    # Convert currency based on 1 usd
                    row_db['value'] = f"{float(row_curr['Value']):,.2f}"
        
                # First symbol in the list
        first_symbol = db_currency_items[0]['symbol']
        first_symbol_value = db_currency_items[0]['value']

        for row in db_currency_items:
            if row['symbol'] == 'USD':
                # swap first symbol with converting symbol and place it on top
                second_symbol = row['symbol']
                second_symbol_value = row['value']

                db_currency_items[0]['symbol'] = row['symbol'] 
                db_currency_items[0]['value'] = row['value']

                row['symbol'] = first_symbol
                row['value'] = first_symbol_value
                
                break

    # Api didn't provide data for a currency
    for row_db in db_currency_items:
        if not row_db['value']:
            row_db['value'] = 'no data'
                

    return db_currency_items

# Return converted currency
def convert_currency(amount, from_currency, to_currency):

    equivalent_amount = amount * to_currency / from_currency
    return equivalent_amount

# Return saved db items
def get_db_items_list():
    # Get saved currency items
    db_currency_items = Currency.objects.all()
    db_currency_items = list(db_currency_items.values())
    
    return db_currency_items