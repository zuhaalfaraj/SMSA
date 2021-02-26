from YahooHistoricalData import YahooFinanceHistory
from DailyStockMarket import StockMarket
from SentimentAnalysis import NewsSentiment

class StockMarketSentimentAnalysis():
    def __init__(self,symbol):
        self.daily_market = StockMarket(symbol)
        self.historical_data = YahooFinanceHistory(symbol)
        self.news_sentiment = NewsSentiment(symbol)

if __name__ =='__main__':
    pass
