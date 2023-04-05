from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from sim_perc_calc import get_similarity_percentage
from nltk import word_tokenize
from nltk.corpus import stopwords
import requests

   
driver = webdriver.Chrome()
url = "https://www.reuters.com/world/russias-arrest-reporter-deepens-bidens-detainee-challenge-2023-04-03/"

driver.get(url)
print('haha')
wait = WebDriverWait(driver, 10)
article = wait.until(EC.presence_of_element_located((By.TAG_NAME, "article")))
print(article.text)
# return links



# trustworthy_response = requests.get(url)
# trustworthy_content = BeautifulSoup(trustworthy_response.content, "html.parser")

# article = trustworthy_content.get('article')

# print(trustworthy_content)
# for link in links:
#     print(link.text)