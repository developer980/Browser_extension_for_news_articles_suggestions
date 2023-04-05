from bs4 import BeautifulSoup
from sim_perc_calc import get_similarity_percentage
from nltk import word_tokenize
from nltk.corpus import stopwords
import requests
from dinamic_scrape import scrape
url = "https://www.reuters.com/site-search/?query=WSJ+reporter+Evan+Gershkovich"

stopwords = set(stopwords.words('english'))

# print(dynamic_content)

# for link in dynamic_content:
#     print(link.get_attribute('href'))

def reuters_data(title_keywords, info_toverify, similarity_score, checked_links, percentage):



    print(title_keywords)
    title_keywords_string = "+".join(title_keywords)
    # title_keywords_string = "reporter+evan+gershkovich+%7C+russia-ukraine+war+news+%7C"
    print("https://www.reuters.com/site-search/?query=" + title_keywords_string)

    links = scrape("https://www.reuters.com/site-search/?query=" + title_keywords_string, 'a')
    print(links)
    # trustworthy_response = requests.get("https://www.reuters.com/site-search/?query=" + title_keywords_string)
    # trustworthy_content = BeautifulSoup(trustworthy_response.content, "html.parser")

    # print(trustworthy_content)
    
    # links = trustworthy_content.find_all("a")

    matches = 0

    # similarity_score = 0
    count = 0;


    # percentage = 0

    for index, link in enumerate(links):
        content = []

        print(link.get_attribute('href'))

        if set(link.text.lower().split(' ')).intersection(set(title_keywords_string.lower().split("+"))):
            print(link.text)
            new_url = link.get_attribute('href')
            
            if new_url not in checked_links:
                
                if "http" in new_url:
                    checked_links.append(new_url)
                    information = requests.get(new_url)
                    information_content = BeautifulSoup(information.content, 'html.parser')
                    # content = information_content.find_all('article')
                    content = scrape(new_url, 'article')
                    print(len(content))
                    score = 0
                    count+=1
                    for index, piece in enumerate(content):
                        
                        words = word_tokenize(piece.text)
                        trustworthy_info = [word for word in words if word not in stopwords]
                        trustworthy_info_string = ' '.join(word for word in trustworthy_info)
                        
                        print(str(len(info_toverify)) + " vs " + str(len(trustworthy_info)))

                        if len(info_toverify) and len(trustworthy_info):

                            # for name in title_names:
                            #     if name in trustworthy_info:
                            #         print(name)

                            if len(info_toverify) < len(trustworthy_info):
                                percentage = get_similarity_percentage(info_toverify, trustworthy_info, similarity_score, percentage)
                                break
                            
                            else:
                                percentage = get_similarity_percentage(trustworthy_info, info_toverify, similarity_score, percentage)
                                break
                
            else:
                print('link already checked')
            # else: continue

    if percentage > 100:
        percentage = 100
    
    return {
        'percentage':percentage,
        'checked_links':checked_links
        }