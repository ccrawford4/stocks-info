from flask import Flask, request, render_template
import requests # Imports the requests library
import os

app = Flask(__name__) # Creates a Flask app with __name__ as parameter because it is the default name for python

# Creates a default route for the flask app
@app.route('/')
def fGetStock(): # Initializes function fGetStock
    return render_template('homepage.html') # Creates an HTML file as a string and then returns the string

@app.route('/stock_result', methods=['GET', 'POST'])
def fPrintStock():
    # HTML header
    top = '''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Response Page</title>
    <meta name="description" content="response">
    <meta name="keywords" content="html sample page">
	</head>'''

    # HTTP Method
    symbol = request.form.get('symbol')

    # Values returned for each checkbox
    opening_value = request.form.get('OpenValue')
    high = request.form.get('High')
    low = request.form.get('Low')
    current_price = request.form.get('CurrPrice')


    # AlphaVantage Stocks API KEY
    API_KEY = os.environ.get('API_KEY')

    # Create request URL
    string = ''
    string += f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&'
    string += f'datatype=csv&apikey={API_KEY}&'
    string += f'symbol={symbol}'


    # Make the request and convert the response into text
    stockResponse = requests.get(string)
    stockResponse = stockResponse.text

    # Response processing
    string = stockResponse.split('\r\n')
    list_keys = []
    list_values = []
    for i in range(len(string)):
        # Put the keys from the first sub list into the dict
        if i == 0:
            string[i] = string[i].split(',')
            for x in string[i]:
                list_keys.append(x)
        else:
        # Put the values from the second sub list into the dict
            string[i] = string[i].split(',')
            for x in range(len(string[i])):
                list_values.append(string[i][x])
                new_dict = dict(zip(list_keys, list_values))

    min = 5     # Stock symbol must be at least 5 characters long

    if len(new_dict) < min:  # Account for when user enters invalid stock symbol
        body = '<p>'
        body += symbol
        body += ' is an invalid stock symbol<br />'
        body += "<a href='/'>Back</a>"
    else:
        body = f'<body>The values for {symbol} are:<br />'

        # Populate the returned HTTP response with the requested values from API
        if opening_value:
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
        body += "<a href='/'>Back</a>"
        body += '</body></html>'

        return top + body

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug='False') # Creates a web server and runs it on port 4999


