import pandas as pd
import nltk
from nltk.corpus import stopwords, wordnet
from nltk import word_tokenize, pos_tag
from nltk.stem import PorterStemmer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
# import spacy
# from nltk
import requests
from bs4 import BeautifulSoup

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('brown')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# https://abc7chicago.com/gwyneth-paltrow-ski-collision-park-city-trial-2023/12985760/"
url = "https://abc7chicago.com/gwyneth-paltrow-ski-collision-park-city-trial-2023/12985760/"
trustworthy_url = "https://www.bbc.co.uk/search?q=GWYNETH+PALTROW"

response = requests.get(url)


stopwords = set(stopwords.words('english'))

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
  print(len(element.text))  
  
for element in info1:
  if len(element.text) > content_size1:
    content_size1 = len(element.text)
  print(len(element.text))  

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

print("The similarity percentage is: " + str(percentage) + " %")
# if matches:
#     print("This article seems genuine")

# else:
#     print("This article seems suspicious")

pars = content_toverify.find_all("div")


# sentiment = SentimentIntensityAnalyzer()
# main_content = []

# for par in pars:
#     text = par.text
    
#     words = nltk.word_tokenize(text)
#     words_count = len(words)

#     if words_count > 100:
#         for word in words:
#             main_content.append(word)

#     filtered_content = [word for word in main_content if word.lower() in stopwords]
#     filtered_content_string = ' '.join(str(word) for word in filtered_content)
#     scores = sentiment.polarity_scores(filtered_content_string)
    
# print(scores)
# if(scores.get('compound') < 0):
#     response = "negative"
# else:
#     response = "positive"

# print("This article seems more " +  response)

# print(title_keywords_string)


# for link in links:
#     print(link.text)


# print(pos_tags)
# nouns = [token.text for token in doc if token.pos_ == "NOUN"]

# blob = TextBlob(sentence)
# keywords = blob.noun_phrases
# print(nouns)


sentence = "GWYNETH PALTROW PARK CITY TRIAL SET TO BEGIN TUESDAY IN DEER VALLEY SKI CRASH CASE"
sentence1 = "Gwyneth Paltrow crash: Skier's daughter tells court he changed after injury"

stemmer = PorterStemmer()

sentence_words = [word.replace("'s", '').replace(":", '') for word in sentence.lower().split() if word not in stopwords]
sentence1_words = [word.replace("'s", '').replace(":", '') for word in sentence1.lower().split() if word not in stopwords]

# print(sentence_words)
# print(sentence1_words)

# word = "ski"
# word1 = "skier"


# for item in wordnet.synsets(word):
#     for item1 in wordnet.synsets(word1):
#         if item.wup_similarity(item1) is not None:
#             print("words are related")
#             break

# print(word_synsets)

word = "judge"
word1 = "trial"



def strings_match(word, word1):
    score = 0

    
    word_synsets = wordnet.synsets(word)
    word1_synsets = wordnet.synsets(word1)

    if word not in word1 and word1 not in word:
        for item in word_synsets:
            for item1 in word1_synsets:
                name = item.name().split(".")[0]
                name1 = item1.name().split(".")[0]

                if item.wup_similarity(item1)>score:
                    score = item.wup_similarity(item1)

        # print(score)

        # return score

        if score > 0.85:
            return True
        else:
            return False
    else:
        return True

match_score = 0;

for word in sentence_words:
    for word1 in sentence1_words:
        if strings_match(word, word1):
            # print(word + " = " + word1)
            strings_match(word, word1)
            match_score += 1

# print(match_score)

# print(strings_match("park", "court"))

common_words = set(sentence_words).intersection(set(sentence1_words))