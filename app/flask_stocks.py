from flask import Flask, request, render_template # Imports Flask, request, and render_template classes from the flask library
import requests # Imports the requests library
import os

app = Flask(__name__) # Creates a Flask app with __name__ as parameter because it is the default name for python

@app.route('/') # Creates a default route for the flask app
def fGetStock(): # Initializes function fGetStock
    return render_template('homepage.html') # Creates an HTML file as a string and then returns the string

@app.route('/stock_result', methods=['GET', 'POST']) # Creates a new app route '/stock_result' with methods 'GET' and 'POST'
def fPrintStock(): # Initalizes a function fPrintStock
    top = '''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Response Page</title>
    <meta name="description" content="response">
    <meta name="keywords" content="html sample page">
	</head>''' # Creates the top string for the HTML page
    symbol = request.form.get('symbol') # Uses requests.form.get to get the inputted value of the symbol
    opening_value = request.form.get('OpenValue') # Uses requests.form.get to get the value of the Open Value checkbox
    high = request.form.get('High') # Uses requests.form.get to get the value of the High checkbox
    low = request.form.get('Low') # Uses requests.form.get to get the value of the Low checkbox
    current_price = request.form.get('CurrPrice') # Uses requests.form.get to get the value of the Currence Price checkbox
    API_KEY = os.environ.get('API_KEY')
    string = '' # Creates an empty string for the link 
    string += f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&' # Adds the first part of the link to the string
    string += f'datatype=csv&apikey={API_KEY}&' # Adds the middle part with the API key to the string
    string += f'symbol={symbol}' # Adds the last part with the symbol to the string
    stockResponse = requests.get(string) # Uses requests library to get the string value from the API key
    stockResponse = stockResponse.text # Converts the returned value into a readable text
    string = stockResponse.split('\r\n') # Splits the string into two different lists
    list_keys = [] # Initalizes an empty list list_keys 
    list_values = [] # Initalizes an empty list list_values
    for i in range(len(string)): # Iterates through the string
        if i == 0: # If it is the first element in the list (ie the keys (symbol, high, low, etc))
            string[i] = string[i].split(',') # Takes the string value and splits it based on the commas
            for x in string[i]: # Iterates through the new nested list
                list_keys.append(x) # Adds each element in the list to the list_keys
        else: # If it is the second element in the list (ie the values)
            string[i] = string[i].split(',') # Splits the string element based on commas
            for x in range(len(string[i])): # Iterates through the new nested list
                list_values.append(string[i][x]) # Adds all the key values into the list_keys
    new_dict = dict(zip(list_keys, list_values)) # Creates a new dictionary with list_keys and list_values as key, values respectivly
    max = 5 # Standard length of dictionary with appropriate symbol
    if len(new_dict) < max: # If the length of the dictionary is less than the appropriate length
        body = '<p>' # Creates a new string with an error message and back link
        body += symbol
        body += ' is an invalid stock symbol<br />'
        body += "<a href='/'>Back</a>"
    else: # If it is an appropriate synmbol
        body = f'<body>The values for {symbol} are:<br />' # Creates the header for the symbol
        if opening_value: # If the checkbox is checked then the string adds the label and value of said checkbox
            body += 'Opening value: '
            body += new_dict['open']
            body += '<br />'
        if high:
            body += 'Highest value: '
            body += new_dict['high']
            body += '<br />'
        if low:
            body += 'Lowest value: '
            body += new_dict['low'] 
            body += '<br />'
        if current_price:
            body += 'Current price: '
            body += new_dict['price']
            body += '<br />'
        body += "<a href='/'>Back</a>" # Adds the back link to the string
        body += '</body></html>' # adds the end of the html file to the string
    return top + body # Returns the string

if __name__ == '__main__': # Sees if the file is the main file 
    app.run(host='0.0.0.0', port= 5000, debug='True') # Creates a web server and runs it on port 4999


