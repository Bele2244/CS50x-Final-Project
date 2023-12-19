# currency
#### Video Demo:  <https://youtu.be/U-vwQHp2QmM>
#### Description:
The app is made as a Harvard CS50x final project with the help of Django, HTML, CSS, JS, and 
Python.  
The app uses Django DB model to save added currencies via a POST request.  
Added symbols are then saved permanently in the Django DB until deleted at the request of the 
user.

### Features

## Add button
User can add new symbols by either typing currency symbol or by typing name of the country  
input data is not case sensitive however all symbols are unique which means you can not add
two countries who are using the same currency symbol, if either one of those symbols is  
already added, the pop will appear to indicate that the symbol is already added for that 
country.      

## Delete button
when delete button is clicked js script is run and will append checkbox for every symbol  
in the list and the list will turn red indicating all available symbols that can be deleted  
user can then delete one or more symbols via POST request by clicking delete after desired  
checkbox symbols are chosen.  
after clicking delete chosen symbols are removed from django DB.

## Convert button
When at least 2 symbols are added to the DB, the 'Convert' button will appear. If  
clicked, it will provide two input fields: the amount of currency to convert  
and a select list with symbols that are already added as options   
When 'Convert' button is clicked, the form data is then cleaned and sent to the 
module function get_symbol_data which will return the converting value of all the symbols  
saved in the django db placing the currency and the amount of the symbol is being converted from 
to the top of the saved symbols list indicating the converting symbol
and the converting symbol amount.
Conversion rates are based on 1 USD. 
Exchange rates data is provided by CurrencyAPI.
however since the api doesn't provide exchange data for all the currencies in the world
symbols can still get added but the exchange rates for that specific symbol are not provided
and therefore can't convert that symbol.

## Get Latest Rates button   
When the 'Get Latest Rates' button is clicked, the call_write_api function is called.
Function calls then call the API. If the call is 
successful, popup message will appear indicating that the api call was success.
Function then writes the latest exchange rates returned from api call to a CSV file
data is then rendered on the index page for all saved symbols in DB.
if Api didn't provide exchange for certain symbol that symbol will have value of 'no data' 
If the Api call fails, then the previous saved exchange rates are rendered on index page.
And the pop message will appear at the top of the list indicating that the api call failed.

## Delete All button
If 'Delete All' is clicked, all saved symbols are deleted from 
the Django DB. 

## Countries Page
The 'Countries page' renders all your symbols as a list of countries that use that
specific currency.
