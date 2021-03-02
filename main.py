from YahooHistoricalData import YahooFinanceHistory
from DailyStockMarket import StockMarket
from SentimentAnalysis import NewsSentiment

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
        self.end_date = date[0]
        return data

    def get_related_historical_data(self):
        self.hestorical_data = self.daily_market.get_historical_data(self.start_date.year, self.start_date.month,
                                              self.start_date.day, self.end_date.year,
                                              self.end_date.month, self.end_date.day)
        return self.hestorical_data

    def get_historical_data(self,start_year,start_month,start_day,end_year,end_month,end_day):
        return self.daily_market.get_historical_data(start_year,start_month,
                                                     start_day,end_year,end_month,end_day)


if __name__ =='__main__':
    smsa= StockMarketSentimentAnalysis('GME')
    print(smsa.get_sentiment())
