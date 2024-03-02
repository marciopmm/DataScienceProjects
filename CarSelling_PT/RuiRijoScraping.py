import requests
from bs4 import BeautifulSoup
from selenium import webdriver

class RuiRijoScraping:
    def __init__(self, url):
        self.url = url

    def get_data(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.find_all('div', class_='col-xs-12 col-sm-6 col-md-4 col-lg')
        print(len(divs))
        driver.close()
        return len(divs)