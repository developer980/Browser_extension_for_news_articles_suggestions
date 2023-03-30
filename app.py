import pandas as pd
import nltk
from nltk.corpus import stopwords, wordnet
from nltk import word_tokenize, pos_tag
from nltk.stem import PorterStemmer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from flask import Flask, render_template, request, jsonify, Response
import json


stopwords = set(stopwords.words('english'))
# import spacy
# from nltk
import requests
from bs4 import BeautifulSoup

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('brown')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

app = Flask(__name__)

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

    title = content_toverify.find('title')
    title_tokens = nltk.word_tokenize(title.text)
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

    if content_size > content_size1:
        content_information = info

    else:
        content_information = info1

    print(content_information)

    # if len(content_information):
    #     print("Length")
    #     print(len(content_information))
    #     print(content_information)

    info_toverify = []
    max_length = 0

    for piece in content_information:
        words = nltk.word_tokenize(piece.text)
        filtered_info = [str(word) for word in words if word not in stopwords]
        if len(filtered_info) > len(info_toverify):
            info_toverify = filtered_info
        # print("article "  + str(len(info_toverify)))

    # print("article" info_toverify)

    title_keywords = [token.replace("'s", '').replace(":", '').lower() for token in title_tokens if token not in stopwords]
    title_keywords_string = "+".join(title_keywords)



    trustworthy_response = requests.get("https://www.bbc.co.uk/search?q=" + title_keywords_string)
    trustworthy_content = BeautifulSoup(trustworthy_response.content, "html.parser")

    links = trustworthy_content.find_all("a")

    matches = 0

    similarity_score = 0
    count = 0;

    for index, link in enumerate(links):
        content = []
        # print(index)
        # print(link.text + ": " + str(len(link.text)))
        # print(link.get('href'))
        if set(link.text.lower().split(' ')).intersection(set(title_keywords_string.lower().split("+"))):
            print(link.get('href'))
            new_url = link.get('href')
            information = requests.get(new_url)
            information_content = BeautifulSoup(information.content, 'html.parser')
            content = information_content.find_all('article')
            print(len(content))
            score = 0
            count+=1
            for index, piece in enumerate(content):
                # print(content.find('div'))
                # if index == 0:
                # print(piece.text)
                words = nltk.word_tokenize(piece.text)
                filtered_piece = [word for word in words if word not in stopwords]
                # print(len(filtered_piece))
                final_result = ' '.join(word for word in filtered_piece)
                # print(len(info_toverify))
                for info in info_toverify:
                    if final_result.find(info) != -1:
                        score += 1
                # if len(filtered_piece):
                # print(filtered_piece)
                print("score: " + str(score))
                if score > similarity_score:
                    similarity_score = score
                break

    print(similarity_score)
    percentage = similarity_score/len(info_toverify) * 100

    obj = {'data':"The similarity percentage is: " + str(percentage) + " %"}
    response = Response(json.dumps(obj), status=200, mimetype='application/json')
    print()
    return response

# https://abc7chicago.com/gwyneth-paltrow-ski-collision-park-city-trial-2023/12985760/"
# url = "https://abc7chicago.com/gwyneth-paltrow-ski-collision-park-city-trial-2023/12985760/"



# if matches:
#     print("This article seems genuine")

# else:
#     print("This article seems suspicious")


if __name__ == '__main__':
    app.run(debug = True)