from unicodedata import name
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import requests
import json
import pandas as pd
from datetime import datetime, timedelta


#Were I to use an api that requires an api key, this is how we would add it
#headers_dict = {'Accepts': 'application/json','X-CMC_PRO_API_KEY': 'cf1c4cb9-f50d-4d2c-8331-0ff5e2f0cc30',}
#r = requests.get('<MY_URI>', headers=headers_dict)


class GraphCreator:
    
    def __init__(self, coin_symbol):
        self.coin_symbol = coin_symbol

    #Having been given a raw response from the api request, convert this into a pd dataframe
    def convert_result_to_pd(self,raw):
        #Convert raw response to a json representation
        data = raw.json()

        #Create a pd dataframe from the json result
        df = pd.DataFrame(data['result']['604800'], columns=['CloseTime', 'OpenPrice', 'HighPrice', 'LowPrice', 'ClosePrice', 'Volume', 'NA'])

        #Make a date out of CloseTime
        df['CloseTime'] = pd.to_datetime(df['CloseTime'], unit='s')

        df['CloseTime']=df['CloseTime'].astype(str)



        return df

    #Check if we can get data about the given symbol on our target exchange
    def check_symbol_exists_on_exchange(self):
        try:
            check_symbol = (requests.get(f'https://api.cryptowat.ch/markets/kraken/{self.coin_symbol}usd/price')).json()

            if "error" in check_symbol and check_symbol["error"]=='Instrument not found':
                return False
            else:
                return True
        except Exception as e:
            print(e)


    def driver_logic(self):

        try:

            if(self.check_symbol_exists_on_exchange()==False):
                return "Symbol doesn\'t exist"
            else:
                print('We should query the api')

                #Converting coin symbol to the lowercase version of itself
                coin_symbol=self.coin_symbol.lower()

                #Creating timestamps for the time period before the coin was listed and 
                from_date=int((datetime.now()- timedelta(weeks = 1080)).timestamp())
                today_date=int((datetime.now()- timedelta(weeks = 12)).timestamp())

                
                #generating request urls to REST api
                data_raw_current = requests.get(f'https://api.cryptowat.ch/markets/kraken/{coin_symbol}usd/ohlc', params={'after':today_date,'periods': '604800'})


                #create pandas dataframe for the price data at the moment
                df = self.convert_result_to_pd(data_raw_current)

                # Remove two columns name is 'C' and 'D'
                df = df.drop(['OpenPrice', 'HighPrice','LowPrice','Volume','NA'], axis=1)

                #Rename columns for frontend
                df = df.rename({'CloseTime': 'x', 'ClosePrice': 'y'}, axis='columns')

                df = df.to_json(orient="records")

                print(df)

                return(df)
        except Exception as e:
            print(e)




    