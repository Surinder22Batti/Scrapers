
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import requests, csv
import time, sys

"""
    Author: SurinderB
    Skills: Python, Django, Flask, Angular, NodeJS, ReactJS, VueJS.
    Email: surinderpal7@gmail.com
    Skype: surinder22.batti
"""

# Chrome webdriver path update here.
chrome_path = '/home/gc14/Downloads/chromedriver'

class ArchitizerHelper():

    def __init__(self):
        self.url = 'https://architizer.com/firms/'
        self.driver = webdriver.Chrome(chrome_path)
        self.driver.maximize_window()

    # method to get items.
    def getItems(self):
        items = []
        try:
            self.driver.get(self.url)
            count = 0
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                count += 1
                print("count : ",count)
                if count >= 267:
                    break
            time.sleep(3)
            soup = BeautifulSoup(self.driver.page_source, u'html.parser')
            # links = self.driver.find_elements_by_xpath("//a[@class='black fw-medium firm-name ellipsis']")
            links = soup.findAll("a", attrs={"class": "black fw-medium firm-name ellipsis"})
            print("links : ",len(links))
            if links:
                count = 0
                for link in links:
                    count += 1
                    data = {}
                    name = link.text.encode("utf-8")
                    try:
                        address = link.find_next_sibling("a").text.encode("utf-8")
                    except:
                        try:
                            address = link.find_next_sibling("span", attrs={"class": "fs-s ellipsis"}).text.encode("utf-8")
                        except:
                            address = None

                    link = link["href"]
                    if "http" not in link:
                        link = "https://architizer.com" + str(link)
                    print("link : ",link, count)

                    res = requests.get(link)
                    soup1 = BeautifulSoup(res.content, u'html.parser')
                    try:
                        email_html = soup1.find("span", attrs={"class": "grey icon mail"})
                        email = email_html.find_next_sibling("span").text.encode("utf-8")
                    except:
                        email = None

                    try:
                        phone_html = soup1.find("span", attrs={"class": "grey icon phone"})
                        phone = phone_html.find_next_sibling("span").text.encode("utf-8")
                    except:
                        phone = None

                    # print("name : ",name)
                    # print("address : ",address)
                    # print("link : ",link)
                    # print("Email : ",email)
                    # print("Phone : ",phone)
                    data.update({'link': link})
                    data.update({'name': name})
                    data.update({'address': address})
                    data.update({'email': email})
                    data.update({'phone': phone})
                    items.append(data)
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!")
        except:
            print(sys.exc_info())
            pass

        self.driver.close()
        
        return items

    
    # method to write data in CSV format
    def write(self, items):
        with open("architizer.csv", mode="w") as csv_file:
            fieldnames = ["URL", "Name", "Address", "Email", "Phone"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for item in items:
                writer.writerow({
                    "URL": item["link"],
                    "Name": item["name"], 
                    "Address": item["address"], 
                    "Email": item["email"], 
                    "Phone": item["phone"],
                })
            csv_file.close()
            print("File written success.")


if __name__ == '__main__':

    # objAH is an instance for ArchitizerHelper
    objAH = ArchitizerHelper()
    items = objAH.getItems()
    if items:
        objAH.write(items)
    else:
        print("Items not found.")