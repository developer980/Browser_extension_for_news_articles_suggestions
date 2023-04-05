from nltk import word_tokenize
from nltk.corpus import stopwords
from bbc_scrape import bbc_data
from reuters_scrape import reuters_data

stopwords = set(stopwords.words('english'))


# def get_percentage(title_keywords, info_toverify):
    
checked_links = []
percentage = 0
similarity_score = 0
title_keywords = "Blinken calls on Russia to release WSJ reporter Evan Gershkovich"
# title_keywords_tokens = word_tokenize(title_keywords.split(" "))
title_filtered_keywords = [word for word in title_keywords.split(" ") if word not in stopwords]

x = len(title_filtered_keywords)
y = 1
print(title_filtered_keywords)
while x > 3:
    length = x
    x = -(-x // 2)
    y = length - x + 1
    last = len(title_filtered_keywords) - (len(title_filtered_keywords) - x)
    first = 0
    
    for i in range(y):
        z = len(title_filtered_keywords)
        new_keywords = [title_filtered_keywords[i] for i in range(first, last) if title_filtered_keywords[i] not in stopwords]
        first += 1
        last += 1;
        print(new_keywords)    

        # response = reuters_data(new_keywords, info_toverify, similarity_score, checked_links, percentage)
        # percentage = response.get('percentage')
        # checked_links = response.get('checked_links')
        # print(percentage)

    # return percentage