import requests # Imports requests library

def main(): # Initializes main function
    symbol = 'AAPL' # Hardcodes the Apple Stock symbol and initalizes it with symbol
    print(fGetStock(symbol)) # Prints the returned value of fGetStock function with symbol as an argument
   


def fGetStock(pSymbol): # Initalizes fGetStock function with pSymbol as a parameter
    string = '' # Creates an empty string
    string += 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&' # Adds to the string the first part of the link
    string += 'datatype=csv&apikey=I0X6GPR31SIUP3MF&' # Adds to the string the second part of the link with API key
    string += f'symbol={pSymbol}' # Adds to string the last part with the pSymbol parameter
    stockResponse = requests.get(string) # Uses requests library to get the value of the API link
    return stockResponse.text # Converts it to a string and returns it 
    



    

main() # Calls main function to start program
