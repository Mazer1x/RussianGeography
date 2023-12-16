from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.options import Options
import time

links = [
    "https://fabricators.ru/proizvodstvo/zavody-plastmass",
    "https://fabricators.ru/proizvodstvo/himicheskie-zavody",
    "https://fabricators.ru/proizvodstvo/zavody-metallokonstrukciy",
    "https://fabricators.ru/proizvodstvo/mashinostroitelnye-zavody"
]

class Parser():
    def __init__(self): #!Инициализация
        options = Options()
        options.page_load_strategy = 'none'
        self.driver = webdriver.Chrome(options=options)
        
        
    
    def getHTML(self): #!Получаем HTML
        driver = self.driver
        return driver.page_source
    
    def isFinal(self,html): #!Последняя ли страница
        soup = BeautifulSoup(html,"lxml")
        next_pager = soup.find("div",class_="pager-next")
        if next_pager.text=="Дальше":
            return False
        else:
            return True
        
    def nextPage(self): #! Перелист страницы
        driver = self.driver
        driver.find_element(By.CLASS_NAME,"pager-next").click()

    def getLinks(self): #! Получаем все ссылки
        driver = self.driver
        for el in driver.find_elements(By.CLASS_NAME,"title-site--h3"):
            link = el.get_attribute("href")
            check = open("Data\links.txt")
            if link+"\n" in check:
                pass
            else:
                check.close()
                file = open("Data\links.txt","a")
                file.write(link+"\n")
                file.close()
            

if __name__=="__main__":
    driver = Parser()
    driver.driver.get(links[3])
    time.sleep(10)
    while True:
        html = driver.getHTML()
        driver.getLinks()
        if not(driver.isFinal(html=html)):
            driver.nextPage()
            time.sleep(10)
        else:
            raise SyntaxError

