from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from tbselenium.tbdriver import TorBrowserDriver 
import time, csv
from random import randint
import os, sys
import psutil, platform
import webbrowser
import subprocess
for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict()
        pid = pinfo['ppid']
        if pinfo['exe'] :
            if "Tor Browser" in pinfo['exe']:
                os.system("taskkill /im firefox /f")
    except psutil.NoSuchProcess:
        pass
# sys.exit(1)

filepath = "/home/gc14/Documents/softwares/tor-browser_en-US/Browser/firefox"
if platform.system() == 'Darwin':       # macOS
    subprocess.call(('open', filepath))
# elif platform.system() == 'Windows':    # Windows
#     os.startfile(filepath)
else:
    pass


chrome_path = "/home/gc14/Documents/fiverr/scrapyapp/scrapyapp/utility/chromedriver"
class ChromeHelper():
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_path)
        self.driver.maximize_window()

    # method to get item (article) detail
    def getItemDetail(self, url):
        print("Going to get page detail by chrome!!!!!!!!!!!!!!!!!!")
        item = {}
        try:
            self.driver.get(url)
            time.sleep(randint(5, 20))

            # try:
            #     google_captcha = self.driver.find_element_by_xpath("//div[@class='g-recaptcha-bubble-arrow']")
            #     if google_captcha:
            #         print("ccccccccccccccccccccccccccccccccccccccccccccc")
            #         self.getItemDetailByFirefox(url)
            # except:
            #     pass

            # self.driver.execute_script("window.localStorage;")
            self.driver.execute_script("localStorage.clear();")
            # print(self.driver.execute_script("return localStorage"))
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")

            try:
                title_info = self.driver.find_element_by_xpath("//meta[@property='og:title']")
                if title_info:
                    title = title_info.get_attribute("content")
            except:
                title = ""

            try:
                comments_info = self.driver.find_element_by_id("a-comments")
                if comments_info:
                    comments = comments_info.find_element_by_xpath(".//a").text
                    comments = comments.replace("comments", "").replace("comment", "").strip()
            except:
                comments = 0
            
            try:
                likes_info = self.driver.find_element_by_xpath("//span[@id='a-comments']/following-sibling::span")
                likes_info = likes_info.find_element_by_xpath(".//div")
                if likes_info:
                    likes = likes_info.get_attribute("data-count")
            except:
                likes = 0

            try:
                followers_info = self.driver.find_element_by_xpath("//div[@class='follow-btn-section']")
                if followers_info:
                    followers = followers_info.text
                    followers = followers.replace("followers", "").replace("follower", "").replace("(", "").replace(")", "").strip()
            except:
                followers = 0

            try:
                author_info = self.driver.find_element_by_id("about_primary_stocks")
                if author_info:
                    author = author_info.text
            except:
                author = ""

            try:
                timing_info = self.driver.find_element_by_xpath("//time[@itemprop='datePublished']")
                if timing_info:
                    timing = timing_info.text
            except:
                timing = ""

            try:
                try:
                    summary_info = self.driver.find_element_by_xpath("//div[@itemprop='description']")
                except:
                    summary_info = self.driver.find_element_by_xpath("//div[@itemprop='articleBody']")
                if summary_info:
                    summary = summary_info.text.encode("utf-8")
            except:
                summary = ""

            item.update({"url": url})
            item.update({"title": title})
            item.update({"comments": comments})
            item.update({"likes": likes})
            item.update({"followers": followers})
            item.update({"author": author})
            item.update({"timing": timing})
            item.update({"summary": summary})
        except:
            print(sys.exc_info())

        self.driver.close()
        print("Crome search completed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return item

class FireFoxHelper():
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()

    def getItemDetail(self, url):
        item = {}
        print("Going to get page detail firefox!!!!!!!!!!!!!!!!!!")
        try:
            self.driver.get(url)
            time.sleep(randint(5, 20))

            try:
                google_captcha = self.driver.find_element_by_xpath("//div[@class='g-recaptcha-bubble-arrow']")
                if google_captcha:
                    print("ccccccccccccccccccccccccccccccccccccccccccccc")
                    objC = ChromeHelper()
                    objC.getItemDetail(url)
            except:
                pass

            # self.driver.execute_script("window.localStorage;")
            self.driver.execute_script("localStorage.clear();")
            # print(self.driver.execute_script("return localStorage"))
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
            
            try:
                title_info = self.driver.find_element_by_xpath("//meta[@property='og:title']")
                if title_info:
                    title = title_info.get_attribute("content")
            except:
                title = ""

            try:
                comments_info = self.driver.find_element_by_id("a-comments")
                if comments_info:
                    comments = comments_info.find_element_by_xpath(".//a").text
                    comments = comments.replace("comments", "").replace("comment", "").strip()
            except:
                comments = 0
            
            try:
                likes_info = self.driver.find_element_by_xpath("//span[@id='a-comments']/following-sibling::span")
                likes_info = likes_info.find_element_by_xpath(".//div")
                if likes_info:
                    likes = likes_info.get_attribute("data-count")
            except:
                likes = 0

            try:
                followers_info = self.driver.find_element_by_xpath("//div[@class='follow-btn-section']")
                if followers_info:
                    followers = followers_info.text
                    followers = followers.replace("followers", "").replace("follower", "").replace("(", "").replace(")", "").strip()
            except:
                followers = 0

            try:
                author_info = self.driver.find_element_by_id("about_primary_stocks")
                if author_info:
                    author = author_info.text
            except:
                author = ""

            try:
                timing_info = self.driver.find_element_by_xpath("//time[@itemprop='datePublished']")
                if timing_info:
                    timing = timing_info.text
            except:
                timing = ""

            try:
                try:
                    summary_info = self.driver.find_element_by_xpath("//div[@itemprop='description']")
                except:
                    summary_info = self.driver.find_element_by_xpath("//div[@itemprop='articleBody']")
                if summary_info:
                    summary = summary_info.text.encode("utf-8")
            except:
                summary = ""

            item.update({"url": url})
            item.update({"title": title})
            item.update({"comments": comments})
            item.update({"likes": likes})
            item.update({"followers": followers})
            item.update({"author": author})
            item.update({"timing": timing})
            item.update({"summary": summary})
        except:
            print(sys.exc_info())

        self.driver.close()
        print("Firefox search End!!!!!!!!!!!!!!!!!!!!!!.")
        return item


class SeekingAlphaHelper():

    def __init__(self):
        # self.url = "https://seekingalpha.com/article/4280759-amd-unwarranted-panic-selling-irrelevant-trump-tweet"
        # self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome(chrome_path)
        
        # tbpath = "/home/gc14/Documents/softwares/tor-browser_en-US"
        # self.driver = TorBrowserDriver(tbb_path=tbpath, tbb_logfile_path='test.log')
        self.driver.maximize_window()
        # self.objF = FireFoxHelper()
        # self.objC = webdriver.Chrome(chrome_path)
        self.temp_urls = [
            "https://jsonplaceholder.typicode.com/posts",
            "https://stackoverflow.com/questions/58261378/image-not-showing-up-on-mobile-devices",
            "https://www.tutorialspoint.com/jquery/jquery-progressbar.htm",
            "https://www.tutorialspoint.com/nodejs/nodejs_buffers.htm",
            "https://realpython.com/python-requests/",
            "https://stackoverflow.com/questions/58420647/python-loop-calculate-sum-between-2-random-values-from-1-10",
            "https://stackoverflow.com/questions/58419896/writing-scrapped-data-into-json-using-python",
            "https://jsonplaceholder.typicode.com/comments",
            "https://www.pythonforbeginners.com/requests/using-requests-in-python",
            "https://www.amazon.in/Amazfit-Lite-Smart-Watch-Black/dp/B07TGDC67L/ref=zg_bs_computers_5?_encoding=UTF8&psc=1&refRID=00Q8Y9X8B260MADDX8T4",
            "https://www.tutorialspoint.com/jquery/jquery-selectors.htm",
            "https://jsonplaceholder.typicode.com/users",
            "https://www.w3schools.com/nodejs/nodejs_events.asp",
            "https://www.tutorialspoint.com/nodejs/nodejs_buffers.htm",
            "https://pypi.org/project/requests/",
        ]

    # method to read the file.
    def readFile(self):
        urls = []
        try:
            # reading csv file 
            with open('/home/gc14/Documents/fiverr/custom_scrapers/home/blogs/seekingalpha-articles.csv', 'r') as csvfile: 
                # creating a csv reader object 
                csvreader = csv.reader(csvfile)
                
                # # extracting field names through first row 
                # fields = csvreader.next() 
            
                # # extracting each data row one by one 
                # for row in csvreader: 
                #     rows.append(row) 
                urls = [url[0] for url in csvreader][1:]
        except:
            pass

        return urls

    def getItems(self, count=0):
        self.by_pass_google_captcha()
        items = []
        urls = self.readFile()
        urls = urls[count:]
        # count = 0
        for url in urls:
            count += 1
            print("Url is : ",url)
            print("count : ",count)
            item = self.getItemDetail(url, count)
            if item:
                items.append(item)
            
            if count >= 5:
                break

            print(item)
            print("!"*100)

        # if self.driver:
        #     self.driver.close()
        return items

    def by_pass_google_captcha(self):
        for url in range(0, 8):
            random_value = randint(url, 10)
            self.driver.get(self.temp_urls[random_value])

    # method to get item (article) detail
    def getItemDetail(self, url, n):
        print("Going to get page detail!!!!!!!!!!!!!!!!!!")
        item = {}
        try:
            self.driver.get(url)
            time.sleep(randint(4, 8))
            try:
                google_captcha = self.driver.find_element_by_xpath("//div[@class='g-recaptcha-bubble-arrow']")
                if google_captcha:
                    print("ccccccccccccccccccccccccccccccccccccccccccccc")
                    self.driver.close()
                    time.sleep(2)
                    
                    # time.sleep(2)
                    n -= 1
                    obj = SeekingAlphaHelper()
                    obj.getItems(count=n)
                    
                    # self.objF.getItemDetail(url)
                    # objC = ChromeHelper()
                    # objC.getItemDetail(url)
                    # self.getItemDetail(url)
            except:
                pass

            # self.driver.execute_script("window.localStorage;")
            self.driver.execute_script("localStorage.clear();")
            # print(self.driver.execute_script("return localStorage"))
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
            try:
                title_info = self.driver.find_element_by_xpath("//meta[@property='og:title']")
                if title_info:
                    title = title_info.get_attribute("content")
            except:
                title = ""

            try:
                comments_info = self.driver.find_element_by_id("a-comments")
                if comments_info:
                    comments = comments_info.find_element_by_xpath(".//a").text
                    comments = comments.replace("comments", "").replace("comment", "").strip()
            except:
                comments = 0
            
            try:
                likes_info = self.driver.find_element_by_xpath("//span[@id='a-comments']/following-sibling::span")
                likes_info = likes_info.find_element_by_xpath(".//div")
                if likes_info:
                    likes = likes_info.get_attribute("data-count")
            except:
                likes = 0

            try:
                followers_info = self.driver.find_element_by_xpath("//div[@class='follow-btn-section']")
                if followers_info:
                    followers = followers_info.text
                    followers = followers.replace("followers", "").replace("follower", "").replace("(", "").replace(")", "").strip()
            except:
                followers = 0

            try:
                author_info = self.driver.find_element_by_id("about_primary_stocks")
                if author_info:
                    author = author_info.text
            except:
                author = ""

            try:
                timing_info = self.driver.find_element_by_xpath("//time[@itemprop='datePublished']")
                if timing_info:
                    timing = timing_info.text
            except:
                timing = ""

            try:
                try:
                    summary_info = self.driver.find_element_by_xpath("//div[@itemprop='description']")
                except:
                    summary_info = self.driver.find_element_by_xpath("//div[@itemprop='articleBody']")
                if summary_info:
                    summary = summary_info.text.encode("utf-8")
            except:
                summary = ""

            item.update({"url": url})
            item.update({"title": title})
            item.update({"comments": comments})
            item.update({"likes": likes})
            item.update({"followers": followers})
            item.update({"author": author})
            item.update({"timing": timing})
            item.update({"summary": summary})
        except:
            print(sys.exc_info())

        return item
    
    # method to write article data in CSV format
    def write(self, items):
        with open("/home/gc14/Documents/fiverr/custom_scrapers/home/blogs/articles.csv", mode="w") as csv_file:
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

    objSAH = SeekingAlphaHelper()
    objSAH.start()
            