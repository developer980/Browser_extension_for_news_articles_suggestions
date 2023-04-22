import pandas as pd
import nltk
from nltk.corpus import stopwords, wordnet
from nltk import word_tokenize, pos_tag
from nltk.stem import PorterStemmer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from flask import Flask, render_template, request, jsonify, Response, send_from_directory
import json
from flask_cors import CORS
import sys
sys.path.append('../')
from scrape.bbc_scrape import bbc_data
# from the_wall_street_scrape import the_wall_street_data
from similarities.get_percentage import get_percentage

stopwords = set(stopwords.words('english'))
# import spacy
# from nltk
import requests
from bs4 import BeautifulSoup
# import sim_perc_calc

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('brown')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ['GET', 'POST'])
def index():
   return render_template('index.html')
@app.route('/post', methods=['GET', 'POST'])
def post():
    req = request.get_json()
    data = json.dumps(req)
    url = json.loads(data)['url']
    print(url)
    response = requests.get(url)


    content_toverify = BeautifulSoup(response.content, "html.parser")

    page_metas = content_toverify.find_all('meta')

    # attributes = page_metas.attrs

    for meta in page_metas:
        attributes = meta.attrs
        # print(meta.attrs)

        for key, value in attributes.items():
            word = 'news'
            if word in value:
                print(value)

    title = content_toverify.find('title')

    if title is None:
        print("doesn't seem an article")
        message = Response(json.dumps({
            'message':'none'
        }), status = 200, mimetype = "application/json")
        return message

    title_tokens = nltk.word_tokenize(title.text)
    title_names = []


    for token in title_tokens:
        if token[0].isupper():
            title_names.append(token)


    headline = content_toverify.find('h1')
    divs = content_toverify.find_all('div')
    hasDay = False
    hasMonth = False

    for div in divs:
        div_tokens = word_tokenize(div.text.lower())
        
        for day in days:
            if day.lower() in div_tokens:
                hasDay = True
                break

        for month in months:
            if month.lower() in div_tokens:
                hasMonth = True
                break

    

    if headline is not None and (hasDay or hasMonth):

        info = content_toverify.find_all("article")
        info1 = content_toverify.find_all("main")
        content_information = info
        content_size = 0
        content_size1 = 0

        for element in info:
            if len(element.text) > content_size:
                content_size = len(element.text)
        # print(len(element.text))  

        for element in info1:
            if len(element.text) > content_size1:
                content_size1 = len(element.text)
        # print(len(element.text))  

        if len(info):
            content_information = info

        else:
            content_information = info1

        info_toverify = []
        max_length = 0

        for piece in content_information:
            words = nltk.word_tokenize(piece.text)
            filtered_info = [str(word) for word in words if word not in stopwords]
            if len(filtered_info) > len(info_toverify):
                info_toverify = filtered_info

        info_toverify_string = ' '.join(word for word in info_toverify)

        # print("article" info_toverify)

        title_keywords = [token.replace("'s", '').replace(":", '').lower() for token in title_tokens if token not in stopwords]
        

        print(title)

        response = get_percentage(title_keywords, info_toverify)
        percentage = response.get('percentage')
        suggestions = response.get('suggestions')
        highest_perc = response.get('highest_percentage_link')
        
        # percentage = the_wall_street_data(title_keywords, info_toverify)
        
        print(title_names)
        # obj = {'data':"The similarity percentage is: " + str(percentage) + " %"}
        obj = Response(json.dumps({
            'percentage':percentage,
            'suggestions':suggestions,
            'highest_perc':highest_perc
            }), status=200, mimetype='application/json')
        # print(obj)
        return obj

    else:
        print("doesn't seem an article")
        message = Response(json.dumps({
            'message':'none'
        }), status = 200, mimetype = "application/json")
        return message

# https://abc7chicago.com/gwyneth-paltrow-ski-collision-park-city-trial-2023/12985760/"
# url = "https://abc7chicago.com/gwyneth-paltrow-ski-collision-park-city-trial-2023/12985760/"




if __name__ == '__main__':
    app.run(debug = True)