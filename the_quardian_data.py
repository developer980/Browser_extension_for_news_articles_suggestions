import sys
import nltk
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import requests
import sim_perc_calc

stopwords = set(stopwords.words('english'))

# https://eu.usatoday.com/story/news/world/2023/04/03/evan-gershkovich-russia-wsj-arrest/11591966002/

url = "https://www.nytimes.com/search?query=Blinken+calls+on+Russia+to+release+WSJ+reporter"

content = requests.get(url)
content_info = BeautifulSoup(content.content, "html.parser")
links = content_info.find_all("a")

for link in links:
    # print(link.text)
    if "http" in link.get("href"):
        link_data = requests.get(link.get("href"))
        link_info = BeautifulSoup(link_data.content, "html.parser")
        content = link_info.find('article')
        print(content.text)
    

# def the_wall_street_data(title_keywords, info_toverify)
#     title_keywords_string = "+".join(title_keywords)
#     # print("https://www.wsj.com/search?query=" + title_keywords_string)
#     trustworthy_response = requests.get("https://www.google.co.uk/search?q=" + title_keywords_string)
#     trustworthy_content = BeautifulSoup(trustworthy_response.content, "html.parser")

#     links = trustworthy_content.find_all("a")

#     matches = 0

#     similarity_score = 0
#     count = 0;


#     percentage = 0

#     for index, link in enumerate(links):
#         content = []

#         # print(link.text)

#         if set(link.text.lower().split(' ')).intersection(set(title_keywords_string.lower().split("%20"))):
            
#             # print("link: " + link.get('href'))
#             new_url = link.get('href')
            
#             if "http" in new_url:
#                 information = requests.get(new_url)
#                 information_content = BeautifulSoup(information.content, 'html.parser')
#                 content = information_content.find_all('article')
#                 # print(content)
#                 score = 0
#                 count+=1
#                 for index, piece in enumerate(content):
                    
#                     words = nltk.word_tokenize(piece.text)
#                     trustworthy_info = [word for word in words if word not in stopwords]

#                     print("length: " + str(len(trustworthy_info)))
#                     trustworthy_info_string = ' '.join(word for word in trustworthy_info)
                    
#                     print(str(len(info_toverify)) + " vs " + str(len(trustworthy_info)))

#                     if len(info_toverify) and len(trustworthy_info):

#                         # for name in title_names:
#                         #     if name in trustworthy_info:
#                         #         print(name)

#                         if len(info_toverify) < len(trustworthy_info):
#                             percentage = sim_perc_calc.get_similarity_percentage(info_toverify, trustworthy_info, similarity_score, percentage)
#                             break
                        
#                         else:
#                             percentage = sim_perc_calc.get_similarity_percentage(trustworthy_info, info_toverify, similarity_score, percentage)
#                             break
            
#             # else: continue

#     if percentage > 100:
#         percentage = 100
    
#     return percentage