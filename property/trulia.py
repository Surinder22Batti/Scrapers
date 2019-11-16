from selenium import webdriver
from bs4 import BeautifulSoup
import requests, random, string
import csv, sys, time
from tbselenium.tbdriver import TorBrowserDriver 
import subprocess, os, platform
import psutil
import webbrowser
for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict()
        # print(pinfo)
        pid = pinfo['ppid']
        if pinfo['exe'] :
            if "Tor Browser" in pinfo['exe']:
                os.system("taskkill /im firefox /f")
    except psutil.NoSuchProcess:
        pass
sys.exit(1)

filepath = "/home/gc14/Documents/softwares/tor-browser_en-US/Browser/firefox"
if platform.system() == 'Darwin':       # macOS
    subprocess.call(('open', filepath))
elif platform.system() == 'Windows':    # Windows
    os.startfile(filepath)
else:
    pass
    # subprocess.call(('xdg-open', filepath)) # linux variants
    # subprocess.Popen(['xdg-open', filepath])
    # webbrowser.open(filepath)
    # webbrowser.get('firefox').open_new_tab('http://www.google.com')

class TruliaHelper():

    def __init__(self):
        self.url = 'https://www.trulia.com'
        # need to set Tor Browser path here.
        tbpath = "/home/gc14/Documents/softwares/tor-browser_en-US"
        self.driver = TorBrowserDriver(tbb_path=tbpath, tbb_logfile_path='test.log')
        # self.driver = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary)
        # self.driver = webdriver.Chrome(executable_path='../utility/chromedriver.exe', chrome_options=chrome_options)

    # method to get items from given link.
    def getItems(self):
        items = []
        # keywords = ['512 W 10th St Perris CA 92570', 'New York, NY', 'San Francisco, CA', 'Washington, CA']
        keywords = ['512 W 10th St Perris CA 92570'] * 2
        for keyword in keywords:
            self.driver.get(self.url)
            search_box = self.driver.find_element_by_id("homepageSearchBoxTextInput")
            search_box.clear()
            search_box.send_keys(keyword)
            search_btn = self.driver.find_element_by_xpath("//button[@data-auto-test-id='searchButton']")
            if search_btn:
                print("Going to click")
                search_btn.click()
                time.sleep(10)
                items.append(self.getItemDetail())

        self.driver.close()
        return items

    def getItemDetail(self):
        data = {}
        try:
            soup = BeautifulSoup(self.driver.page_source, u'html.parser')
            image = soup.find("div", attrs={"class": "Tiles__TileBackground-fk0fs3-0 cSObNX"}).find("img")["src"]
            price = soup.find("div", attrs={"class": "Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 hlvKRM"}).text
            # container = soup.find("div", attrs={"class": "resultsColumn"}).find("ul")
            # items = container.findAll("li", recursive=False)
            data.update({
                "image": image,
                "price": price
            })
        except:
            pass
        return data

    # method to write csv file
    def writeCSVFile(self, data):
        try:
            with open('/home/gc14/Documents/fiverr/custom_scrapers/home/trulia.csv', mode='w') as csv_file:
                fieldnames = ['Image', 'Price']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for d in data:
                    writer.writerow({'Image': d['image'], 'Price': d['price']})
                csv_file.close()
            print("File written successfully.")
        except:
            print(sys.exc_info())
            pass

    # method to start process.
    def start(self):
        items = self.getItems()
        print("Items : ",len(items))
        if items:
            self.writeCSVFile(items)

# main function call
if __name__ == "__main__":

    # objTH is an TruliaHelper class.
    objTH = TruliaHelper()
    objTH.start()