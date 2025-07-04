import pprint
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects, HTTPError
import json
import keys
import traceback

pp = pprint.PrettyPrinter(indent=4)

# ID:
# BTC: 1
# ETH: 1027
# SOL: 5426
# MOB: 7878
# FTT: 4195
# BEAN: 12503
# GOLD: 3575
# PAXG: 4705
# JUP 29210


class Crypto(object):
    def __init__(self, *args, **kwargs):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        self.parameters = {
          'convert':'USD',
          # 'symbol':'SUSDe,BTC,ETH,SOL,GOLD,PAXG,SILVER'
          'id':'29471,1,1027,5426,3575,4705,32419'
            
          #'id':'29210,1,1027,5426'
            
        }
        self.headers = {
          'Accepts': 'application/json',
          'X-CMC_PRO_API_KEY': keys.coinmarketcap_key,
        }

    def get_crypto_quotes(self):
        session = Session()
        session.headers.update(self.headers)

        response = session.get(self.url, params=self.parameters)
        response.raise_for_status()

        data = json.loads(response.text)

        watched_tickers = {"SUSDe":"29471","BTC":"1", "ETH":"1027", "SOL":"5426","PAXG":"4705","SILVER":"32149"}
        reported_tickers = {}
        crypto_list = data["data"]

        for symbol,id in watched_tickers.items():
            if not id in crypto_list:
                continue
            crypto = crypto_list[id]
            current_price = crypto["quote"]["USD"]["price"]
            daily_volume = crypto["quote"]["USD"]["volume_24h"]
            daily_percent_change = crypto["quote"]["USD"]["percent_change_24h"]

            reported_tickers[symbol] = {}
            reported_tickers[symbol]["price"] = current_price
            reported_tickers[symbol]["volume"] = daily_volume
            reported_tickers[symbol]["change"] = daily_percent_change

        status_string = ""
        status_tuples = []
        for reported_ticker, values in reported_tickers.items():
            trend = "↓"
            trend_status = "down"
            if reported_ticker == "GOLD":
                status_string = reported_ticker + ": " + "unknown "
                status_tuples.append((status_string, trend_status))
                print(status_string)
                continue
            elif values["change"] is None:
                status_string = reported_ticker + ": " + "unknown "
                status_tuples.append((status_string, trend_status))
                print(status_string)
                continue
            if values["change"]>=0:
                trend = "↑"
                trend_status = "up"

            status_string = reported_ticker + ": " + "$" + "{:.2f}".format(values["price"]) + " "  + trend + " {:.2f}".format(values["change"]) + "%  "
            status_tuples.append((status_string, trend_status))
            
            print(status_string)
        return(status_tuples)

    def getMap(self):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        parameters = {
          # 'convert':'USD'z,
          # 'symbol':'BTC,ETH,SOL,MOB'
          # 'id':'1,1027,5426'
        }
        session = Session()
        session.headers.update(self.headers)

        response = session.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/map", params=parameters)
        response.raise_for_status()

        data = json.loads(response.text)
        return data




if __name__ == "__main__":
    ticker = Crypto()
    pp.pprint(ticker.getMap())
    pp.pprint(ticker.get_crypto_quotes())
