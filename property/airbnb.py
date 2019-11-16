import requests, time
from bs4 import BeautifulSoup

# https://www.airbnb.com/c/surinderp126?currency=INR earning link

class AirbnbHelper():
    def __init__(self):
        self.url = "https://www.airbnb.com/s/Chandigarh--Punjab/homes?refinement_paths%5B%5D=%2Fhomes&toddlers=0&query=Chandigarh%2C%20Punjab&search_type=unknown&zoom=9&search_by_map=true&sw_lat=30.361263699496057&sw_lng=75.35491329101569&ne_lat=30.944871651527603&ne_lng=76.75841670898444&adults=2&children=2&place_id=ChIJ72ppYKZpEDkRaxAVduWJxzs&s_tag=loerix0m"

        
    def getItems(self):
        res = requests.get(self.url)
        soup = BeautifulSoup(res.content, "html.parser")
        time.sleep(3)
        items = soup.findAll("div", attrs={"class": "_1s4ejkyh"})
        print("items : ",len(items))

    def getItemDetail(self, url):
        url = "https://www.airbnb.com/rooms/5215842?location=Chandigarh%2C%20Punjab&toddlers=0&adults=2&children=2&home_collection=1&source_impression_id=p3_1564863387_lLTYOi3qu%2BVh2M9r&s=a_r2jP1_"
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "html.parser")
        title = soup.find("span", attrs={"class": "_18hrqvin"}).text
        address = soup.find("div", attrs={"class": "_czm8crp"}).text
        # price = soup.find("span", attrs={"class": "_doc79r"}).text
        images = soup.find("div", attrs={"class": "_167bw5o"}).findAll("img")
        description = soup.find("p", attrs={"class": "_6z3til"}).text
        reviews = soup.find("span", attrs={"class": "_s1tlw0m"}).text
        rating = soup.find("div", attrs={"itemprop": "ratingValue"})["content"]
        author = soup.find("div", attrs={"class": "_8b6uza1"}).text
        author_img = soup.find("img", attrs={"class": "_1mgxxu3"})["src"]
        print("title : ",title)
        print("address : ",address)
        # print("price : ",price)
        print("description : ",description)
        print("reviews : ",reviews)
        print("rating : ",rating)
        print("images : ",len(images))
        print("author : ",author)
        print("author_img : ",author_img)

if __name__ == "__main__":
    objAH = AirbnbHelper()
    objAH.getItems()