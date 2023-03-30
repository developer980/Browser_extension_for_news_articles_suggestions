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