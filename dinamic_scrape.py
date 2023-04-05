from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from sim_perc_calc import get_similarity_percentage
from nltk import word_tokenize
from nltk.corpus import stopwords
import requests


def scrape(url, obj):    
    driver = webdriver.Chrome()
    driver.get(url)
    print('haha')
    wait = WebDriverWait(driver, 10)
    links = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, obj)))
    print(links)
    return links

# scrape("https://www.reuters.com/site-search/?query=WSJ+reporter+Evan+Gershkovich")