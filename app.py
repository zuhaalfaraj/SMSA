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
app = Flask(__name__)

def plot_sentiment(ticker):
    global smsa
    smsa = StockMarketSentimentAnalysis(ticker)
    sentiment_data = smsa.get_sentiment()
    mean_df = sentiment_data.groupby('date').mean()
    mean_df= mean_df.reset_index()
    data = [
        go.Bar(
            name='sentiment index',
            x= mean_df['date'],
            y=mean_df['sentiment']
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
            marker={'color': 'red'}
        )
    ]

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

    return render_template('index.html', ticker= text, plot=bar,plot_2= bar_2,
                           price=price, change=change, market_cap=market_cap,
                           open_price=open_price, range=range)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()