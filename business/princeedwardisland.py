from selenium import webdriver
import requests
from bs4 import BeautifulSoup

import time, csv
from random import randint
import os, sys

chrome_path = "/home/gc14/Documents/fiverr/scrapyapp/scrapyapp/utility/chromedriver"
class ChromeHelper():
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_path)
        self.driver.maximize_window()
        self.url = "https://www.princeedwardisland.ca/en/feature/pei-business-corporate-registry#/?e=BusinessAPI&name=aaa&page_num=1&page_count=1&finished=0"

    def getItems(self):
        items = []
        self.driver.get(self.url)
        page_txt = self.driver.find_element_by_xpath("//div[@id='reusable-app']")
        total_items = 0
        if page_txt:
            page_txt = page_txt.find_element_by_xpath(".//p[@class='text']")
            if page_txt:
                total_items = page_txt.text.split("of")[-1].strip()
                total_items = int(total_items)

        pages = 0
        if total_items:
            pages = total_items / 20
            if total_items % 20 > 0:
                pages += 1

        print("pages : ",pages)

        urls = []
        for page in range(1, pages+1):
            try:
                url = "https://www.princeedwardisland.ca/en/feature/pei-business-corporate-registry#/?e=BusinessAPI&name=aaa&page_num=1&page_count=1&finished=0&page_number=" + str(page) + "&page_size=20"
                self.driver.get(url)
                time.sleep(2)
                table = self.driver.find_element_by_xpath("//table[@class='table null']")
                if table:
                    rows = table.find_elements_by_xpath(".//tbody/tr")
                    urls.extend([row.find_element_by_xpath(".//td/a").get_attribute("href") for row in rows])
            except:
                print(sys.exc_info())

        # print("items : ",items)
        print("urls : ",len(urls))
                
        count = 0
        for url in urls:
            count += 1
            print("Url is : ",url)
            print("count : ",count)
            # item = self.getItemDetail(url)
            # if count >= 10:
            #     break

            print("!"*100)
        self.driver.close()
        return items

    # method to get item (article) detail
    def getItemDetail(self, url):
        print("Going to get page detail by chrome!!!!!!!!!!!!!!!!!!")
        item = {}
        self.driver.get(url)
        time.sleep(randint(3, 10))
        
        try:
            title_info = self.driver.find_element_by_xpath("//meta[@property='og:title']")
            if title_info:
                title = title_info.get_attribute("content")
        except:
            title = ""

        item.update({"url": url})
        item.update({"title": title})

        self.driver.close()
        return item

     
    # method to write article data in CSV format
    def write(self, items):
        with open("/home/gc14/Documents/fiverr/custom_scrapers/home/blogs/articles4.csv", mode="w") as csv_file:
            fieldnames = ["URL", "Title", "Author", "Comments", "Likes", "Followers", "Date", "Summary"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for item in items:
                writer.writerow({
                    "URL": item["url"],
                    "Title": item["title"], 
                    "Author": item["author"], 
                    "Comments": item["comments"], 
                    "Likes": item["likes"], 
                    "Followers": item["followers"], 
                    "Date": item["timing"], 
                    "Summary": item["summary"]
                })
            csv_file.close()
            print("File written success.")
            
    def start(self):
        items = self.getItems()
        print("Total Items : ",len(items))
        if items:
            self.write(items)
        else:
            print("Items not found.")
        

if __name__ == "__main__":

    objCH = ChromeHelper()
    objCH.start()
            