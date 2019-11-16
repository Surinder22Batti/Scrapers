# -*- coding: utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import sys, time

class BehanceHelper():

    def __init__(self):
        # self.driver = webdriver.PhantomJS('/home/gc14/Downloads/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        self.driver = webdriver.Chrome("/home/gc14/Documents/fiverr/scrapyapp/scrapyapp/utility/chromedriver") 

    # method to get profile data.
    def getProfileDetail(self, item_url):
        try:
            self.driver.get(item_url)
            time.sleep(5)
            # page = self.driver.page_source
            # with open('sample.html', 'w') as f:
            #     f.write(page)
            #     f.close()
            soup = BeautifulSoup(self.driver.page_source, u'html.parser')
            # headline = self.driver.find_element_by_id('profile-title').text
            headline = soup.find("div", attrs={"id": "profile-title"})
            headline = str(headline.text).strip()
            print "headline : ",headline
            about_me = soup.find("meta", attrs={"name": "description"})['content']
            print "about_me : "
            print about_me

            # resume_res = requests.get('https://www.behance.net/bhavaniprasadkarrotu/resume')
            resume_link = self.driver.find_element_by_id('')
            if resume_link:
                resume_link = resume_link.click()
                time.sleep(5)
            resume_soup = BeautifulSoup(self.driver.page_source, u'html.parser')
            user_detail_sections = resume_soup.findAll('div', attrs={'class': 'section'})
            print "user_detail_sections : ",len(user_detail_sections)
            if len(user_detail_sections):
                experience = []
                education = []
                skills = []
                for section in user_detail_sections:
                    name = section.find('h1').text.encode('utf-8').strip()
                    if 'Work Experience' in name:
                        exp_levels = section.findAll('div', attrs={'class': 'module'})
                        if len(exp_levels):
                            for level in exp_levels:
                                exp_org = level.find("h2", attrs={'class': 'organization'}).text
                                if exp_org:
                                    exp_org = exp_org.encode('utf-8').strip()

                                exp_position = level.find("h3", attrs={'class': 'position'}).text
                                if exp_position:
                                    exp_position = exp_position.encode('utf-8').strip()
                                time_period = level.find('div', {'class': 'time-location'}).find('span', {'class': 'time'})
                                time_period = time_period.text.encode('utf-8').strip()
                                
                                time_period = str(time_period).split('-')
                                start_date = time_period[0].strip()
                                end_date = time_period[1].strip()
                                location = level.find('div', attrs={'class': 'time-location'}).find('span', {'class': 'location'})
                                location = location.text.encode('utf-8').strip()
                                experience.append({
                                    'title': exp_position,
                                    'organisation': exp_org,
                                    'start_date': start_date,
                                    'end_date': end_date,
                                    'location': location
                                })
                        
                    elif 'Education' in name:
                        edu_levels = section.findAll('div', attrs={'class': 'module'})
                        if len(edu_levels):
                            for level in edu_levels:
                                edu_org_n = level.find("h2", attrs={'class': 'organization'})
                                if edu_org_n:
                                    k = str(edu_org_n.text).strip()
                                    if len(k) <= 0:
                                        edu_org = edu_org_n.find('a')['href']
                                    else:
                                        edu_org = edu_org_n.text.encode('utf-8').strip()
                                
                                edu_position = level.find("h3", attrs={'class': 'position'}).text
                                if edu_position:
                                    edu_position = edu_position.encode('utf-8').strip()
                                
                                time_period = level.find('div', {'class': 'time-location'}).find('span', {'class': 'time'})
                                time_period = time_period.text.encode('utf-8').strip()
                                time_period = str(time_period).split('-')
                                start_date = time_period[0].strip()
                                end_date = time_period[1].strip()

                                location = level.find('div', attrs={'class': 'time-location'}).find('span', {'class': 'location'})
                                location = location.text.encode('utf-8').strip()
                                education.append({
                                    'title': edu_position,
                                    'organisation': edu_org,
                                    'start_date': start_date,
                                    'end_date': end_date,
                                    'location': location
                                }) 
            elif 'Skills' in name:
                skills_levels = section.findAll('div', attrs={'class': 'module'})
                if len(skills_levels):
                    for level in skills_levels:
                        skills_data = level.find("div", attrs={'class': 'skills'})
                        if skills_data:
                            skills_data = skills_data.text.encode('utf-8').strip()
                        
                        skills.append({'skills': skills_data})
            print "experience : "
            print experience
            print "education : "
            print education
            print "skills : "
            print skills
        except:
            print sys.exc_info()
            pass

        # close webdriver session
        self.driver.close()

    # method to store data in file.
    def saveJSONfile(self, data):
        try:
            print 
        except:
            pass

    def start(self):
        print 'wwwwwwww'
        item_url = 'https://www.behance.net/bhavaniprasadkarrotu'
        data = self.getProfileDetail(item_url)
        print data
        # if data:
        #     self.saveJSONfile(data)
        print '#'*100

# main function
if __name__ == '__main__':
    # objBH is an instance for BehanceHelper.
    objBH = BehanceHelper()
    objBH.start()