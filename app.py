from flask import Flask, render_template, request
import base64
from io import BytesIO
from matplotlib.figure import Figure
import numpy as np
import plotly
import plotly.graph_objs as go
import json
import pandas as pd
import plotly.express as px
from main import StockMarketSentimentAnalysis
import requests
from sklearn.preprocessing import StandardScaler
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

def plot_sentiment(ticker):
    global smsa
    smsa = StockMarketSentimentAnalysis(ticker)
    sentiment_data = smsa.get_sentiment()
    mean_df = sentiment_data.groupby('date').mean()[:-1]
    mean_df= mean_df.reset_index()
    data = [
        go.Bar(
            name='sentiment index',
            x= mean_df['date'],
            y=mean_df['sentiment'],
        marker = {'color': 'Gold'}
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def plot_h_date():
    h_data= smsa.get_related_historical_data()
    data = [
        go.Bar( name='price difference',
            x= h_data['Date'][1:],
            y=h_data['Close'].diff()[1:],
            marker={'color': 'DarkSeaGreen'}
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
def plot_price_vs_sent():
    h_data= smsa.get_related_historical_data()
    h_data_std = StandardScaler().fit_transform(h_data[['Close', 'Open']].diff()[1:])
    sentiment_data = smsa.get_sentiment()
    sentiment_data = sentiment_data.groupby('date').mean()
    sentiment_data= sentiment_data.reset_index()

    data_1 = [
        go.Bar(
            name='std historical change',
            x=h_data['Date'][1:],
            y= pd.Series(h_data_std[:,0]),
            marker={'color': 'DarkSeaGreen'}
        )
    ]
    data_2 = [
        go.Bar(
            name='sentiment index',
            x= sentiment_data['date'],
            y=sentiment_data['sentiment'],
            marker={'color': 'Gold'}

        )
    ]
    graphJSON_1 = json.dumps(data_1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_2 = json.dumps(data_2, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON_1, graphJSON_2



def plot_pie():
    values= smsa.get_sentiment_cat()
    labels= ['positive news', 'negative news', 'natural']
    colors = ['LightSalmon', 'LightCoral', 'LightBlue']

    data= [go.Pie(labels=labels, values=values, marker=dict(colors=colors))]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def plot_pie_change():
    values= smsa.get_perc_change()
    labels= ['<-25%','-25% to -1%','0% to 25%','25% to 50%','50%-100%', '>100%']
    colors = ['PeachPuff', 'RosyBrown', 'Moccasin', 'Linen', 'LemonChiffon', 'Lavender']
    data= [go.Pie(labels=labels, values=values, marker=dict(colors=colors))]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    smsa = StockMarketSentimentAnalysis(text)
    data = smsa.get_pre_data()
    price= str(data['price'])
    change = data['change']
    market_cap=data['market_cap']
    open_price= data['open_price']
    range= data['range']
    print(price)

    bar = plot_sentiment(text)
    bar_2 = plot_h_date()
    pie_sent= plot_pie()
    pie_change=plot_pie_change()
    hst, sent= plot_price_vs_sent()

    return render_template('index.html', ticker= text, plot=bar,plot_2= bar_2,pie_sent=pie_sent,
                           pie_change=pie_change,hst=hst,sent=sent,
                           price=price, change=change, market_cap=market_cap,
                           open_price=open_price, range=range)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()