from selenium import webdriver
from bs4 import BeautifulSoup
import time, sys

"""
    Author: SurinderB
    Skills: Python, Django, Flask, Angular, NodeJS, ReactJS, VueJS.
    Email: surinder22.batti@gmail.com
    Skype: surinder22.batti 
"""


# Chrome webdriver path update here.

chrome_path = '/home/gc14/Documents/fiverr/scrapyapp/scrapyapp/utility/chromedriver'

class IndeedHelper():

    def __init__(self):
        self.url = 'https://www.indeed.co.in'
        self.driver = webdriver.Chrome(chrome_path)

    # method to get items.
    def getItems(self):
        try:
            self.driver.get(self.url)
            search_field = self.driver.find_element_by_id("text-input-what")
            search_field.send_keys("Software Developer")
            search_button = self.driver.find_element_by_xpath("//button[@type='submit']")
            search_button.click()
            time.sleep(2)
            page = 1
            self.getPageDetail(self.driver.current_url, page)
            pages = self.driver.find_element_by_id("searchCountPages")
            if pages:
                pages = str(pages.text).split("of")[-1].replace("jobs", "").replace("job", "").strip()
            print("Pages : ",pages)

            while True:
                try:
                    page += 1
                    next_button = self.driver.find_element_by_xpath("//div[@class='pagination']")
                    next_button = next_button.find_elements_by_xpath(".//span[@class='np']")[-1]
                    if 'next' in str(next_button.text.encode('utf-8')).lower():
                        self.driver.execute_script("arguments[0].click();", next_button)
                        self.getPageDetail(self.driver.current_url, page)
                    else:
                        break
                except:
                    print(sys.exc_info())
                    break
            
                if page >= 5: # update pages limit or comment this code
                    break
        except:
            print(sys.exc_info())
            pass

        self.driver.close()

    # method to store the items. Items stores in CSV, Excel, text, Database.
    def getPageDetail(self, url, page):
        print("Going to get page " + str(page) + " detail")
        print(url)
        print("#"*100)


if __name__ == '__main__':

    # objIH is an instance for IndeedHelper
    objIH = IndeedHelper()
    objIH.getItems()