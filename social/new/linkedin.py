from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import requests, csv
import sys, time
opts = Options()
opts.set_headless()

class LinkedInHelper():
    def __init__(self):
        self.url = "https://www.linkedin.com/mynetwork/invite-connect/connections/"
        self.driver = webdriver.Firefox(options=opts)
        self.driver.maximize_window()
        self.authenticate()

    # method to authenticate user.
    def authenticate(self):
        self.driver.get("https://www.linkedin.com/login")
        self.driver.find_element_by_id("username").send_keys("") # set username here
        self.driver.find_element_by_id("password").send_keys("") # set password here
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(2)

    # method to get user connections.
    def getConnections(self):
        connections = []
        try:
            self.driver.get(self.url)
            time.sleep(3)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            section = soup.find("div", attrs={"class": "core-rail"})
            total = 0
            total_info = section.find("header")
            if total_info:
                total = total_info.text.strip()
            print("total : ",total)
            connections = section.findAll("li", attrs={"class": "list-style-none"})
        except:
            print(sys.exc_info())

        self.driver.quit()
        return connections

    # method to get user connection profile.
    def getProfile(self, connection):
        detail = {}
        try:
            first_name = ""
            last_name = ""
            email = ""
            company = ""
            profile_link = connection.find("a")["href"]
            if "http" not in profile_link:
                profile_link = "https://www.linkedin.com" + profile_link
            contact = profile_link
                
            self.driver.get(profile_link)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            name_info = soup.find("li", attrs={"class": "inline t-24 t-black t-normal break-words"})
            if name_info:
                names = name_info.text.strip().split()
                if len(names) >= 2:
                    first_name = names[0].strip()
                    last_name = names[1].strip()
                else:
                    first_name = name_info.text.strip()
            
            company_info = soup.find("li", attrs={"class": "pv-top-card-v3--experience-list-item"})
            if company_info:
                company = company_info.text.strip()
            
            contact_info = self.driver.find_element_by_xpath("//a[@data-control-name='contact_see_more']")
            if contact_info:
                contact_info = self.driver.execute_script("arguments[0].click();", contact_info)
                time.sleep(3)
                email_info = self.driver.find_element_by_xpath("//section[@class='pv-contact-info__contact-type ci-email']")
                if email_info:
                    email = email_info.find_element_by_xpath(".//a").text
            detail.update({"first_name": first_name})
            detail.update({"last_name": last_name})
            detail.update({"email": email})
            detail.update({"contact": contact})
            detail.update({"company": company})
        except:
            print(sys.exc_info())

        return detail

    # method to write the data in CSV format.
    def write(self, results):
        with open('linkedin.csv', mode='w') as csv_file:
            fieldnames = ["First Name", "Last Name", "Email", "Contact", "Company"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for result in results:
                writer.writerow({"First Name": result["first_name"], "Last Name": result["last_name"], "Email": result["email"], "Contact": result["contact"], "Company": result["company"]})
            csv_file.close()
        print("File written successfully.")

    def start(self):
        results = []
        connections = self.getConnections()
        print("connections : ",len(connections))
        if connections:
            count = 0
            for connection in connections:
                count += 1
                result = self.getProfile(connection)
                print(result)
                if result:
                    results.append(result)
                print("count : ",count)
            if results:
                self.write(results)
        else:
            print("No connection found.")

if __name__ == "__main__":
    objLH = LinkedInHelper()
    objLH.start()

