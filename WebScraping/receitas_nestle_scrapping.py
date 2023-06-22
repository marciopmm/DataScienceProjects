# !pip3 install beautifulsoup4

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import time

def getRecipies(url):
    options = ChromeOptions()
    #options.headless = True

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    while(True):
        moreBtn = driver.find_element(By.ID, 'load_more')
        if moreBtn:
            time.sleep(10)
            moreBtn.click()
            time.sleep(10)
        else:
            break

mainUrl = 'https://www.receitasnestle.com.br/nossas-receitas'
mainText = requests.get(mainUrl).text
soup = BeautifulSoup(mainText, 'lxml')
list_a = soup.find_all('a', class_="item")
a_list = [a['href'] for a in list_a]

for a in a_list:
    getRecipies(urljoin(mainUrl, a))


    
    #categorySoup = BeautifulSoup(driver.page_source, 'lxml')
    #continueBtn = categorySoup.find('a', { 'id': 'load_more'})
