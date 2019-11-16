# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from tbselenium.tbdriver import TorBrowserDriver
import random, sys, time
from fake_useragent import UserAgent

ua = UserAgent(cache=False)
user_agent = ua.random

options = Options()
options.add_argument("window-size=1400,600")
options.add_argument('user-agent='+str(user_agent))

class RealtorHelper():

    def __init__(self):
        self.url = 'https://www.realtor.com'
        # self.driver = webdriver.PhantomJS('/home/gc14/Downloads/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        chrome_path = "/home/gc14/Documents/fiverr/scrapyapp/scrapyapp/utility/chromedriver"
        self.driver = webdriver.Chrome(chrome_path, chrome_options=options) 
        
        # need to set Tor Browser path here.
        # tbpath = "/home/gc14/Documents/softwares/tor-browser_en-US"
        # self.driver = TorBrowserDriver(tbb_path=tbpath, tbb_logfile_path='test.log')
    
    def getItems(self):
        items = []
        try:
            keywords = ["New York, NY"] * 100
            count = 0
            for keyword in keywords:
                count += 1
                print "Going to count : ",count
                self.driver.get(self.url)
                search_input = self.driver.find_element_by_id("rdc-main-search-nav-hero-input")
                search_input.clear()
                search_input.send_keys(keyword)
                search_btn = self.driver.find_element_by_xpath("//button[@class='rdc-btn_2q8dK rdc-btn-brand_28UWP search-btn']")
                if search_btn:
                    search_btn.click()
                    time.sleep(random.randint(0, 10))
                    soup = BeautifulSoup(self.driver.page_source, u'html.parser')
                    try:
                        items_container = soup.find("ul", attrs={"class": "srp-list-marginless list-unstyled prop-list"})
                    except:
                        items_container = soup.find("ul", attrs={"id": "radius-properties"})
                    items_list = items_container.findAll("li")
                    print "items_list : ",len(items_list)
                    if items_list:
                        for item in items_list:
                            price = item.find("span", attrs={"class": "data-price"})
                            if price:
                                items.append(price.text)
                time.sleep(random.randint(0, 5))
        except:
            print sys.exc_info()
            pass

        # close webdriver session
        # self.driver.close()
        return items

    def start(self):
        items = self.getItems()
        print "items : ",len(items)
        print '#'*100

# main function
if __name__ == '__main__':
    # objRH is an instance for RealtorHelper.
    objRH = RealtorHelper()
    objRH.start()