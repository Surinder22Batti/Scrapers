from selenium import webdriver
from bs4 import BeautifulSoup
import random, time, sys
import xlsxwriter, requests
from datetime import datetime,timedelta
import datetime

class FacebookHandler():

    def __init__(self):
        self.url = "https://www.facebook.com/krcgenk/"
        self.driver = webdriver.Chrome('chromedriver')
        self.driver.get('https://www.facebook.com/krcgenk/')
        self.driver.maximize_window()
        self.authenticate()
        self.current_date = datetime.datetime.now()

    # method to authenticate facebook user.
    def authenticate(self):
        try:
            self.driver.get(self.url)
            # Authenticate User
            self.driver.find_element_by_id("email").send_keys("infothreeg@gmail.com")
            self.driver.find_element_by_id("pass").send_keys("puneet6644")
            self.driver.find_element_by_id("u_0_3").click()
            time.sleep(2)
        except:
            pass

    # method to get facebook posts.
    def getPosts(self):
        posts = []
        try:
            self.driver.get(self.url)

            for scroll in range(5):
                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(2)

            # Click on all comments
            comment_links = self.driver.find_elements_by_xpath("//div[@class='_3w53']")
            for comment_link in comment_links:
                comment_link = comment_link.find_element_by_xpath(".//a")
                if comment_link:
                    self.driver.execute_script("arguments[0].click();", comment_link)
                time.sleep(3)

            time.sleep(5)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            posts = soup.find_all('div', attrs = {'class':'userContentWrapper'})
        except:
            print("Error in getPosts function")
            print(sys.exc_info())

        return posts

    # method to get post comments detail.
    def getCommentDetail(self, post):
        comment_details = {}
        try:
            comments = post.find("ul", attrs={"class": "_7791"})
            if comments:
                comments = comments.findAll("li")
                comment_details.update({"count": len(comments)})
                # print("comments : ",len(comments))
                auth_data = ""
                for comment in comments:
                    comment_data = {}
                    
                    try:
                        author_name = comment.find("a", attrs={"class": "_6qw4"}).text
                    except:
                        author_name = ""
                     
                    try:
                        message = comment.find("div", attrs={"class": "_72vr"})
                        message = message.find("span").text
                    except:
                        message = ""

                    try:
                        comment_date = comment.find("span", attrs={"class": "timestampContent"}).text
                    except:
                        try:
                            comment_date = comment.find("abbr", attrs={"class": "livetimestamp"}).text
                        except:
                            comment_date = ""
                    
                    comment_data.update({"comments_count": len(comments)})
                    comment_data.update({"author_name": author_name})
                    comment_data.update({"message": message})
                    comment_data.update({"comment_date": comment_date})
                    if len(author_name) > 0 and len(message) > 0:
                        comment_details.update({"items": comment_data})
                        d = "Name : " + str(author_name) + "\n" + " Message : " + str(message) + " | \n"
                        auth_data += d
                auth_data = auth_data.strip()[:-2]
                comment_details.update({"comments": auth_data})
        except:
            print("Error in getCommentDetail")
            print(sys.exc_info())

        return comment_details
    
    # method to get post detail.
    def getPostDetail(self, post):
        post_detail = {}
        try:
            post_desc = post.find('p').text
            post_date = post.find('abbr',attrs={'class':'_5ptz'}).text
            if "hrs" in post_date:
                hrs = post_date.replace("hrs", "").strip()
                hrs = int(hrs)
                post_date = (self.current_date - datetime.timedelta(hours = hrs))
                post_date = str(post_date.strftime('%Y-%m-%d %H:%M:%S'))
            if "yesterday" in post_date:
                post_date = (self.current_date - datetime.timedelta(days = 1))
                post_date = str(post_date.strftime('%Y-%m-%d %H:%M:%S'))
            author = "KRC Genk official"
            post_detail.update({"author": author})
            post_detail.update({"description": post_desc})
            post_detail.update({"post_date": post_date})
        except:
            print("Error in get Post detail")
            print(sys.exc_info())

        return post_detail

    # method to get post reaction detail.
    def getPostReaction(self, post):
        reaction_data = {
            "like": {
                "count": 0,
                "authors": ""
            },
            "love": {
                "count": 0,
                "authors": ""
            },
            "wow": {
                "count": 0,
                "authors": ""
            }, 
            "haha": {
                "count": 0,
                "authors": ""
            }
        }
        try:
            like_link = post.find('span', attrs ={'data-testid':'UFI2ReactionsCount/sentenceWithSocialContext'})
            if like_link:
                like_link = like_link.find_parent("a")["href"]
                if "http" not in like_link:
                    like_link = "https://www.facebook.com" + str(like_link)
                print("like_link : ",like_link)

                self.driver.get(like_link)

                time.sleep(5)
                like_soup = BeautifulSoup(self.driver.page_source, "html.parser")
                content = like_soup.find("div", attrs={"id": "js_1"})
                if content:
                    reactions = content.find("ul").findAll("li", recursive=False)
                    print("reactions : ",len(reactions))
                    if len(reactions):
                        for reaction in reactions:
                            react_type = reaction.find("div").text
                            if "Like" in react_type:
                                likes = reaction.find("ul").findAll("li", recursive=False)
                                print("likes : ",len(likes))
                                like_authors = ""
                                if likes:
                                    for like in likes:
                                        like_author = like.find("div", attrs={"class": "_5i_t"})
                                        like_author = like_author.find("a").text
                                        like_author = like_author + " | "
                                        # print("like_author : ",like_author)
                                        like_authors += like_author
                                    if like_authors:
                                        like_authors = like_authors[:-2]
                                    reaction_data["like"]["count"] = len(likes)
                                reaction_data["like"]["authors"] = like_authors
                            if "Love" in react_type:
                                loves = reaction.find("ul").findAll("li", recursive=False)
                                print("loves : ",len(loves))
                                love_authors = ""
                                if loves:
                                    for love in loves:
                                        love_author = love.find("div", attrs={"class": "_5i_t"})
                                        love_author = love_author.find("a").text
                                        love_author = love_author + " | "
                                        # print("love_author : ",love_author)
                                        love_authors += love_author
                                    if love_authors:
                                        love_authors = love_authors[:-2]
                                    reaction_data["love"]["count"] = len(loves)
                                reaction_data["love"]["authors"] = love_authors
                            if "Wow" in react_type:
                                wows = reaction.find("ul").findAll("li", recursive=False)
                                print("wows : ",len(wows))
                                wow_authors = ""
                                if wows:
                                    for wow in wows:
                                        wow_author = wow.find("div", attrs={"class": "_5i_t"})
                                        wow_author = wow_author.find("a").text
                                        wow_author = wow_author + " | "
                                        # print("wow_author : ",wow_author)
                                        wow_authors += wow_author
                                    if wow_authors:
                                        wow_authors = wow_authors[:-2]
                                    reaction_data["wow"]["count"] = len(wows)
                                reaction_data["wow"]["authors"] = wow_authors
                            if "Haha" in react_type:
                                hahas = reaction.find("ul").findAll("li", recursive=False)
                                print("hahas : ",len(hahas))
                                haha_authors = ""
                                if hahas:
                                    for haha in hahas:
                                        haha_author = haha.find("div", attrs={"class": "_5i_t"})
                                        haha_author = haha_author.find("a").text
                                        haha_author = haha_author + " | "
                                        # print("haha_author : ",haha_author)
                                        haha_authors += haha_author
                                    if haha_authors:
                                        haha_authors = haha_authors[:-2]
                                    reaction_data["haha"]["count"] = len(hahas)
                                reaction_data["haha"]["authors"] = haha_authors
        except:
            print("Error in get comments : ")
            print(sys.exc_info())

        return reaction_data

    # method to write file.
    def writeFile(self, items):
        print("Going to write file")
        try:
            workbook = xlsxwriter.Workbook('fb2-data.xlsx')
            worksheet = workbook.add_worksheet()
            worksheet.write(0, 0, 'S.No.')
            worksheet.write(0, 1, 'Post Author')
            worksheet.write(0, 2, 'Post')
            worksheet.write(0, 3, 'Post Date')
            worksheet.write(0, 4, 'No. of comments')
            worksheet.write(0, 5, 'Like Count')
            worksheet.write(0, 6, 'Love Count')
            worksheet.write(0, 7, 'Wow Count')
            worksheet.write(0, 8, 'Haha Count')
            worksheet.write(0, 9, 'Comments')
            worksheet.write(0, 10, 'User Who Likes the Post')
            worksheet.write(0, 11, 'User Who Loves the Post')
            worksheet.write(0, 12, 'User Who wow the Post')
            worksheet.write(0, 13, 'User Who haha the Post')

            row = 0
            for item in items:
                row += 1
                worksheet.write(row,0, item["count"])
                worksheet.write(row,1, item["author"])
                worksheet.write(row,2, item["message"])
                worksheet.write(row,3, item["post_date"])
                worksheet.write(row,4, item["comments_count"])
                worksheet.write(row,5, item["like_count"])
                worksheet.write(row,6, item["love_count"]) 
                worksheet.write(row,7, item["wow_count"])
                worksheet.write(row,8, item["haha_count"])
                worksheet.write(row,9, item["comments"])
                worksheet.write(row,10, item["like_authors"])
                worksheet.write(row,11, item["love_authors"])
                worksheet.write(row,12, item["wow_authors"])
                worksheet.write(row,13, item["haha_authors"])
        except:
            print(sys.exc_info())
        finally:
            workbook.close()
        print("File written successfuly.")

    def start(self):
        posts = self.getPosts()
        print("Total Posts : ",len(posts))
        if len(posts):
            post_items = []
            count = 1
            for post in posts:
                print("count : ",count)
                post_data = {}
                post_detail = self.getPostDetail(post)
                if post_detail:
                    print("ppppppppppppppppppppp")
                    print(post_detail)

                    post_comments = self.getCommentDetail(post)
                    if len(post_comments) == 0:
                        time.sleep(3)
                        post_comments = self.getCommentDetail(post)
                    print("dddddddddddddddddd")
                    print(post_comments)

                    post_reactions = self.getPostReaction(post)
                    print("rrrrrrrrrrrrrrrrr")
                    print(post_reactions)
                    if len(post_comments) > 0:
                        # print("like_count", post_reactions["like"]["count"])
                        # print("love_count", post_reactions["love"]["count"])
                        # print("wow_count", post_reactions["wow"]["count"])
                        # print("haha_count", post_reactions["haha"]["count"])

                        post_data.update({"count": count})
                        post_data.update({"author": post_detail["author"]})
                        post_data.update({"message": post_detail["description"]})
                        post_data.update({"post_date": post_detail["post_date"]})
                        
                        post_data.update({"comments_count": post_comments["count"]})
                        post_data.update({"comments": post_comments["comments"]})
                        post_data.update({"like_count": post_reactions["like"]["count"]})
                        post_data.update({"love_count": post_reactions["love"]["count"]})
                        post_data.update({"wow_count": post_reactions["wow"]["count"]})
                        post_data.update({"haha_count": post_reactions["haha"]["count"]})

                        post_data.update({"like_authors": post_reactions["like"]["authors"]})
                        post_data.update({"love_authors": post_reactions["love"]["authors"]})
                        post_data.update({"wow_authors": post_reactions["wow"]["authors"]})
                        post_data.update({"haha_authors": post_reactions["haha"]["authors"]})
                        post_items.append(post_data)
                        count += 1
                time.sleep(random.randint(5, 30))
                print("#"*100)
                # if count >= 3:
                #     break
                

            ############ File write code ####################
            if post_items:
                self.writeFile(post_items)
            else:
                print("Data not found.")
        else:
            print("No post found")

if __name__ == "__main__":
    objFH = FacebookHandler()
    objFH.start()




