# SMSA: Stock Market Sentiment Analysis
<img src="logo.png" width="200">


## An Overview
SMSA is an "analysis tool for the US stock market". The platform mainly focuses on the sentiment behinds the news and how it reflects on the stock price and vice/versa. This is where the name came from (Stock Market Sentiment Analysis).

Web Scrapping was used to acquire data from Yahoo Finance and get news as well. Moreover, NLP layer was used to classify the news based on how good or how bad they are. Finally, the dashboard was built using Flask + Plotly.


## Demo
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/8fsmJagyWpc/0.jpg)](https://www.youtube.com/watch?v=8fsmJagyWpc)

## Requirements
beautifulsoup4==4.9.3  
bs4==0.0.1  
Flask==1.1.2  
lxml==4.6.2  
nltk==3.5  
numpy==1.20.1  
pandas==1.2.2  
plotly==4.14.3  
response==0.5.0  
scikit-learn==0.24.1  
scipy==1.6.0  
Scrapy==1.7.3  
seaborn==0.11.1  
selenium==3.141.0  
sklearn==0.0  
spacy==3.0.3  

## Setup
- Create an environment
```
virtualenv smsaEnv

source smsaEnv/bin/activate
```
- Install requirements
```
pip install requirements.txt
```
- Run the app
```
python app.py
```

## Diagram
<img src="smsa.png" width="700">
