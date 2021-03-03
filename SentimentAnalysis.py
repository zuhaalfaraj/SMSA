from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
class NewsSentiment:
    def __init__(self,symbol):
        url= 'https://finviz.com/quote.ashx?t={0}'.format(symbol)
        req = Request(url=url, headers={'user-agent': 'my-app'})
        response = urlopen(req)
        self.soup = BeautifulSoup(response, features='html.parser')
        self.vader = SentimentIntensityAnalyzer()

    def get_news_data(self):
        df= pd.DataFrame({'title':[],'date':[], 'time':[], 'sentiment':[]})
        table= self.soup.find('table', id='news-table')

        for i,row in enumerate(table.find_all('tr')):
            title = row.a.text
            sentiment= self.vader.polarity_scores(title)['compound']


            date_data= row.td.text.split(' ')
            if len(date_data)==1:
                time= date_data[0]
            if len(date_data) == 2:
                date = date_data[0]
                time = date_data[1]
            data = {'title':title,'date':date, 'time':time,'sentiment':sentiment}
            df= df.append(data, ignore_index=True)

        df['date'] = pd.to_datetime(df.date).dt.date
        self.df = df
        return df

    def get_cat(self):
        pos= self.df[self.df['sentiment']>0]
        neg = self.df[self.df['sentiment']<0]
        natural= self.df[self.df['sentiment']==0]
        return (pos, neg, natural)





