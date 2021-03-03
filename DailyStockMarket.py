import bs4
import requests
import YahooHistoricalData
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class StockMarket():
    def __init__(self,symbol):
        self.url = f'https://finance.yahoo.com/quote/{symbol}'
        self.h_yahoo= YahooHistoricalData.YahooFinanceHistory(symbol)

    def get_data(self):
        re= requests.get(self.url)
        soup= bs4.BeautifulSoup(re.text, 'lxml')
        current_stock={
        'price':soup.find('div', {'class':"D(ib) Mend(20px)"}).find_all('span')[0].get_text(),
        'change': soup.find('div', {'class':"D(ib) Mend(20px)"}).find_all('span')[1].get_text(),
        'market_cap': soup.find('td',{'data-test': "MARKET_CAP-value"} ).find('span').get_text(),
        'open_price': soup.find('td', {'data-test': "OPEN-value"}).find('span').get_text(),
        'range': soup.find('td', {'data-test': "FIFTY_TWO_WK_RANGE-value"}).get_text()

        }
        return current_stock

    def get_historical_data(self,start_year,start_month,start_day,end_year,end_month,end_day):
        datefrom= int(datetime.timestamp(datetime(start_year, start_month, start_day)))
        dateto= int(datetime.timestamp(datetime(end_year, end_month, end_day)))
        df=self.h_yahoo.get_quote(datefrom,dateto)
        return df

    def get_one_year_history(self):
        today= datetime.now()
        ltm = datetime.now() - relativedelta(years=1)
        ltm_date= self.get_historical_data(ltm.year, ltm.month,ltm.day,
                                 today.year, today.month, today.day)
        return ltm_date
