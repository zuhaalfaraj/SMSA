from YahooHistoricalData import YahooFinanceHistory
from DailyStockMarket import StockMarket
from SentimentAnalysis import NewsSentiment
import datetime
class StockMarketSentimentAnalysis:
    def __init__(self,symbol):
        self.daily_market = StockMarket(symbol)
        self.historical_data = YahooFinanceHistory(symbol)
        self.news_sentiment = NewsSentiment(symbol)

    def get_pre_data(self):
        return self.daily_market.get_data()

    def get_sentiment(self):
        data = self.news_sentiment.get_news_data()
        date = data['date'].unique()
        self.start_date = date[-1]
        self.end_date = datetime.datetime.today()
        return data

    def get_related_historical_data(self):
        self.hestorical_data = self.daily_market.get_historical_data(self.start_date.year, self.start_date.month,
                                              self.start_date.day, self.end_date.year,
                                              self.end_date.month, self.end_date.day)

        return self.hestorical_data

    def get_historical_data(self,start_year,start_month,start_day,end_year,end_month,end_day):
        return self.daily_market.get_historical_data(start_year,start_month,
                                                     start_day,end_year,end_month,end_day)

    def get_sentiment_cat(self):
        cat = self.news_sentiment.get_cat()
        return [len(cat[0]), len(cat[1]), len(cat[2])]

    def get_perc_change(self):
        x = self.daily_market.get_one_year_history()
        x['change'] = x['Close'].apply(lambda i: i / x['Close'].loc[0] * 100 - 100)

        drop_25 = len(x[x['change']<0][x['change']>=-25])
        drop_more=len(x['change'][x['change']>-25])
        to_25 = len(x['change'][x['change']>0][x['change']<=25])
        to_50= len(x['change'][x['change']>25][x['change']<=50])
        more_50 = len(x['change'][x['change']>50][x['change']<=100] )
        more_100= len(x['change'][x['change']>100])

        return [drop_more,drop_25,to_25,to_50,more_50,more_100]



if __name__ =='__main__':
    smsa= StockMarketSentimentAnalysis('GME')
    print(smsa.get_sentiment())
