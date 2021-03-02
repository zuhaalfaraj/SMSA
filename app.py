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


def plot_historical(ticker):
    smsa= StockMarketSentimentAnalysis(ticker)
    data= smsa.get_historical_data(2020,2,2,2020,6,6)
    open = data['Open']
    close = data['Close']
    high = data['High']
    low = data['Low']
    date = data['Date']

    data = [
        px.line(
            x= date,
            y=close
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

    bar = create_plot()

    return render_template('index.html', plot=bar, price=price, change=change, market_cap=market_cap,
                           open_price=open_price, range=range)

def create_plot():


    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe


    data = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()