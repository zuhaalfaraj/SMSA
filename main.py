import bs4
import requests
import YahooHistoricalData
from datetime import datetime, timedelta

class StockMarket():
    def __init__(self,symbol):
        self.url = f'https://finance.yahoo.com/quote/{symbol}'
        self.history=self.url+'/history'
        self.h_yahoo= YahooHistoricalData.YahooFinanceHistory(symbol)
        print(self.history)


    def get_data(self):
        re= requests.get(self.url)
        soup= bs4.BeautifulSoup(re.text, 'lxml')
        current_stock={
        'price':soup.find('div', {'class':"D(ib) Mend(20px)"}).find_all('span')[0].get_text(),
        'change': soup.find('div', {'class':"D(ib) Mend(20px)"}).find_all('span')[1].get_text()
        }
        return current_stock

    def get_historical_data(self,start_year,start_month,start_day,end_year,end_month,end_day):
        datefrom= int(datetime.timestamp(datetime(start_year, start_month, start_day)))
        dateto= int(datetime.timestamp(datetime(end_year, end_month, end_day)))
        df=self.h_yahoo.get_quote(datefrom,dateto)
        return df



sm= StockMarket('FB')
print(sm.get_historical_data(2020,10,10,2020,10,15))