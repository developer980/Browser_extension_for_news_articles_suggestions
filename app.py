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

url = "https://abc7chicago.com/gwyneth-paltrow-ski-collision-park-city-trial-2023/12985760/"
# https://www.wilx.com/content/news/Study-claims-Nutella-can-cause-cancer-410500595.html
# "https://time.com/6263099/alison-roman-sweet-enough-interview/"

trustworthy_url = "https://www.bbc.co.uk/search?q=GWYNETH+PALTROW"

response = requests.get(url)


stopwords = set(stopwords.words('english'))

content_toverify = BeautifulSoup(response.content, "html.parser")

title = content_toverify.find('title')
title_tokens = nltk.word_tokenize(title.text)

title_keywords = [token.replace("'s", '').replace(":", '').lower() for token in title_tokens if token not in stopwords]
title_keywords_string = "+".join(title_keywords)
trustworthy_response = requests.get("https://www.bbc.co.uk/search?q=" + title_keywords_string)

trustworthy_content = BeautifulSoup(trustworthy_response.content, "html.parser")

links = trustworthy_content.find_all("a")

matches = 0

for link in links:
    print(link.text + ": " + str(len(link.text)))
    print(link.get('href'))
    if set(link.text.lower().split(' ')).intersection(set(title_keywords_string.lower().split("+"))):
        matches+=1
    
if matches:
    print("This article seems genuine")

else:
    print("This article seems suspicious")


# for link in links:
#     print(link.text)

main_content = []

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

print(sentence_words)
print(sentence1_words)

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
            print(word + " = " + word1)
            strings_match(word, word1)
            match_score += 1

print(match_score)

print(strings_match("park", "court"))

common_words = set(sentence_words).intersection(set(sentence1_words))

sentiment = SentimentIntensityAnalyzer()
neg = 0
neu = 0
pos = 0
compound = 0
scores = ()

pars = content_toverify.find_all("div")


for par in pars:
    text = par.text
    
    words = nltk.word_tokenize(text)
    words_count = len(words)

    if words_count > 100:
        for word in words:
            main_content.append(word)

    filtered_content = [word for word in main_content if word.lower() in stopwords]
    filtered_content_string = ' '.join(str(word) for word in filtered_content)
    scores = sentiment.polarity_scores(filtered_content_string)
    
print(scores)
if(scores.get('compound') < 0):
    response = "negative"
else:
    response = "positive"

print("This article seems more " +  response)

print(title_keywords_string)


