from django.shortcuts import render, redirect
from . models import Currency
from . forms import CurrencyForm
from django.http import JsonResponse
from django.contrib import messages

# Local modules
from . check_get_data import check_symbol
from . check_get_data import get_symbol_country
from . check_get_data import get_symbol_value
from . check_get_data import get_db_items_list
from . csv_handler import load_csv
from . call_write_api import call_write_api

# load local csv file
file_country = 'currency/static/country_data.csv'
file_currency = 'currency/static/latest_currency.csv'
country_info = load_csv(file_country)
currency_info = load_csv(file_currency)

# Create your views here.
def index_view(request): 
    
    if request.method == "POST":
        # Get value of the clicked button
        button_clicked = request.POST.get('button', None)

        # Second add button
        if button_clicked == 'add_db_item':

            form_data = CurrencyForm(request.POST or None)
            if form_data.is_valid():
                # Get form symbol          
                form_symbol = request.POST.get('symbol', None)
                # Check form symbol
                valid_symbol = check_symbol(country_info, form_symbol)
                # Current symbols saved in database
                db_currency_items = Currency.objects.all()
                # Symbol is valid 
                if valid_symbol:
                    duplicate = 0
                    # db is not empty
                    if db_currency_items.exists():
                        for currency in db_currency_items:
                            if currency.symbol == valid_symbol:
                                duplicate = 1
                                messages.success(request, ('Symbol already added')) 
                    if not duplicate:
                        # Save to database
                        currency_model = Currency()
                        currency_model.symbol = valid_symbol
                        currency_model.save()
                        messages.success(request, ('Symbol added Successfully!'))
                # Symbol is invalid
                else: 
                    messages.success(request, ('Symbol/Country could not be found!'))
            else:
                messages.success(request, ('Currency/Country Field can not be empty'))
                # First convert button

        # Second convert button
        elif button_clicked == 'convert_currency':
            convert_amount = request.POST.get('convert_amount')
            convert_symbol = request.POST.get('convert_symbol')
            
            # Validate user input
            if len(convert_amount) > 16:
                messages.success(request, ('Number is too big, max number accepted 999.999.999.999'))
                return redirect('index')
            elif convert_amount:
                try:
                    convert_amount = float(convert_amount)
                except ValueError:
                    messages.success(request, ('Please enter a valid number'))
                    return redirect('index')
                else:
                    # Get saved currency items
                    db_currency_items = get_db_items_list()
                    
                    symbol_value = get_symbol_value(db_currency_items, currency_info, convert_amount, convert_symbol)
                    return render(request, 'index.html', {
                        'symbol_value': symbol_value,
                    })

        # Second delete button
        elif button_clicked == 'remove_db_item':
 
            # Clean the form input
            removed_symbols = {}
            for key, value in request.POST.items():
                if len(value) == 3:
                    removed_symbols[key] = value
            
            # Post request for item removal is not empty
            removed_symbols_len = len(removed_symbols)
            
            if removed_symbols_len:
                # Remove desired items
                for value in removed_symbols:
                    removed_value = Currency.objects.filter(symbol=value)
                    removed_value.delete()
                messages.success(request, (f'Deleted {removed_symbols_len} Successfully!'))

            else:
                messages.success(request, ('Select Currency you wish to delete!'))
        
        # Get latest rates button
        elif button_clicked == 'get_latest_ex_rates':
            # Get latest currency rates from api call
            db_currency_items = get_db_items_list()

            # Return message if no symbols are added
            if len(db_currency_items) == 0:
                messages.success(request, ('No symbols added'))
            else:
                call_success = call_write_api()
                if call_success:
                # Get saved currency items
                    db_currency_items = get_db_items_list()
                    symbol_value = get_symbol_value(db_currency_items, currency_info)
                    
                    # Api call successful
                    messages.success(request, ('Success! - Showing latest exchange rates'))
                    
                    return render(request, 'index.html', {
                        'symbol_value': symbol_value,
                    })
                else:
                    # Get saved currency items
                    db_currency_items = get_db_items_list()
                    symbol_value = get_symbol_value(db_currency_items, currency_info)
                    
                    messages.success(request, ('Failed! - Showing old exchange rates'))
                    return render(request, 'index.html', {
                        'symbol_value': symbol_value,
                    })

        # Delete all button is pressed - remove all items from database
        elif button_clicked == 'delete_all_db_item':
            db_currency_items = get_db_items_list()
            db_items_len = len(db_currency_items) 
            Currency.objects.all().delete()
            messages.success(request, (f'Deleted {db_items_len} Successfully!'))

        # Show index page after operation
        return redirect('index')
    
    else:
        # Return all items from database
        symbol_value = get_db_items_list()
        # Render returned items
        return render(request, 'index.html', {
            'symbol_value': symbol_value,
        })

# Get all countries where added currency is used
def countries_view(request):
    
    db_currency_items = get_db_items_list()
    all_countries = []
    for row in db_currency_items:
        symbol = row['symbol']
        symbol_countries = get_symbol_country(country_info, symbol)

        all_countries_symbol = {}
        all_countries_symbol['symbol'] = symbol
        all_countries_symbol['countries'] = symbol_countries

        all_countries.append(all_countries_symbol)
    
    return render(request, 'countries.html', 
                  {'all_countries': all_countries})


def about_view(request):
    
    return render(request, 'about.html')