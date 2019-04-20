"""Get stock data for a single stock ticker"""

import urllib.request
import re

def grab_stock(ticker = 'ZUO'):
    """Get data for a single ticker
    
    :param ticker: [description], defaults to 'ZUO'
    :type ticker: str, optional
    :return: [description]
    :rtype: [type]
    """
    react_ids = {'Price': 14, 'Prev Close': 15, 'Open': 20, 'Volume': 43, 'Avg Volume': 48, 
                'Beta': 61, 'PE Ratio (TTM)': 66, 'EPS (TTM)': 71, '1y Target Est': 90,
                "Day's Range": 34, "52 Week Range": 38, "Market Cap": 56, 'Ex-Dividend Date': 85}

    output = {}
    output['Symbol'] = ticker.upper()

    #return yahoo finance of ticker as data
    url = "https://finance.yahoo.com/quote/%s?p=%s" % (ticker, ticker)
    request = urllib.request.urlopen(url)
    data = request.read().decode()

    # test_taken = []

    for key in react_ids.keys():
        pat = re.compile(r'(?<=data-reactid="' + str(react_ids[key]) + '">)(\d|B|\+| |\-|\-|,|\.)+?(?=<)')
        matches = re.search(pat, data)
        try:
            output[key] = matches.group()
        except AttributeError:
            #output[key] = 'ERROR'
            pass

    return output