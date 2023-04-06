import sys
import nltk
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import requests
import sim_perc_calc

stopwords = set(stopwords.words('english'))

def bbc_data(title_keywords, info_toverify, similarity_score, checked_links, percentage, suggestions, highest_percentage_link):

    # highest_percentage_link = {}
    print(title_keywords)
    title_keywords_string = "+".join(title_keywords)

    trustworthy_response = requests.get("https://www.bbc.co.uk/search?q=" + title_keywords_string)
    trustworthy_content = BeautifulSoup(trustworthy_response.content, "html.parser")

    links = trustworthy_content.find_all("a")

    matches = 0

    # similarity_score = 0
    count = 0;


    # percentage = 0

    for index, link in enumerate(links):
        content = []

        if set(link.text.lower().split(' ')).intersection(set(title_keywords_string.lower().split("+"))):
            print(link.get('href'))
            if link.get("href") is not None and checked_links is not None:
                if link.get('href') not in checked_links:

                    new_url = link.get('href')
                    
                    if "http" in new_url:
                        checked_links.append(link.get('href'))
                        link_content = {
                            'link_text':link.text,
                            'link_href':link.get('href')
                        }

                        if link_content not in suggestions:
                            suggestions.append(link_content)

                        information = requests.get(new_url)
                        information_content = BeautifulSoup(information.content, 'html.parser')
                        content = information_content.find_all('article')
                        print(len(content))
                        score = 0
                        count+=1
                        for index, piece in enumerate(content):
                            
                            words = nltk.word_tokenize(piece.text)
                            trustworthy_info = [word for word in words if word not in stopwords]
                            trustworthy_info_string = ' '.join(word for word in trustworthy_info)
                            
                            print(str(len(info_toverify)) + " vs " + str(len(trustworthy_info)))

                            if len(info_toverify) and len(trustworthy_info):

                                # for name in title_names:
                                #     if name in trustworthy_info:
                                #         print(name)
                                response = {}
                                if len(info_toverify) < len(trustworthy_info):
                                    response = sim_perc_calc.get_similarity_percentage(info_toverify, trustworthy_info, similarity_score, percentage)
                                    percentage = response.get('percentage')
                                    is_the_highest = response.get("is_the_highest") 
                                    print("value: " + str(response.get("is_the_highest")))
                                    if is_the_highest == 1:
                                        print('its high')
                                        highest_percentage_link = {
                                            'text':link.text,
                                            'href':link.get('href')
                                        }
                                        print("the link is:")
                                        print(highest_percentage_link)
                                    break
                                
                                else:
                                    response = sim_perc_calc.get_similarity_percentage(trustworthy_info, info_toverify, similarity_score, percentage)
                                    percentage = response.get('percentage')
                                    is_the_highest = response.get("is_the_highest") 
                                    print("value: " + str(response.get("is_the_highest")))
                                    if is_the_highest == 1:
                                        print('its high')
                                        highest_percentage_link = {
                                            'text':link.text,
                                            'href':link.get('href')
                                        }
                                        print("the link is:")
                                        print(highest_percentage_link)
                                    break

                    
                    else:
                        print('link already checked')

    if percentage > 100:
        percentage = 100
    
    print(highest_percentage_link)
    if highest_percentage_link is not None:
        return {
            'percentage':percentage,
            'suggestions':suggestions,
            'highest_percentage_link':highest_percentage_link
        }
    
    else:
        return {
            'percentage':percentage,
            'suggestions':suggestions,
            'highest_percentage_link':{}
        }