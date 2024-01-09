import requests
from bs4 import BeautifulSoup
from lxml import etree
import json
import re

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

class Openrice:

    def __init__(self, url):

        self.__restaurant_data = list()
        self.__url = url
        self.__page = requests.get(self.__url, headers=headers)
        self.__soup = BeautifulSoup(self.__page.content, "html.parser")
        self.__dom = etree.HTML(str(self.__soup))

    # get 30 most popular restaurant name and its page url
    def restaurants_name(self):
        
        link_elements = self.__dom.xpath('//div[@class="poi-chart-main-grid-item-deskop-title-row-left-section-poi-info-name"]')
        for element in link_elements:

            name = element.xpath(".//text()")[0].replace("\n", "").strip()

            href = element.xpath(".//@href")[0]

            self.__restaurant_data.append(
                {"restaurant_name" : name, 
                 "restaurant_url" : f"https://www.openrice.com{href}/reviews"}
            )

    def restaurant_review(self):
        
        review_user = self.__dom.xpath('//div[@itemprop="author"]')
        comments = self.__dom.xpath('//div[@itemprop="description"]')
        num_of_page = self.__dom.xpath('//*[@id="sr2-review-container"]/div[3]/div/a')

        for i in range(len(comments)):

            username = review_user[i].xpath(".//text()")[1].strip()
            user_review = comments[i].xpath(".//text()")[0]
            user_review = user_review.replace("\r\n", "").strip()
            user_review = self.emoji_filter(user_review)

            self.__restaurant_data.append(
                {"username" : username, 
                 "user_review" : user_review}
            )

        next_button_class = num_of_page[-1].xpath(".//@class")[0]
        next_page_path = num_of_page[-1].xpath(".//@href")[0]

        if next_button_class == "pagination-button next js-next":
            self.__restaurant_data.append({"next_page_url" : f"https://www.openrice.com{next_page_path}"})

    def get_restaurant_data(self): 
        return json.dumps(self.__restaurant_data, ensure_ascii=False).encode('utf8')

    def emoji_filter(self, text):

        try:
            # Wide UCS-4 build
            myre = re.compile(u'['
                            u'\U0001F300-\U0001F64F'
                            u'\U0001F680-\U0001F6FF'
                            u'\u2600-\u2B55'
                            u'\u23cf'
                            u'\u23e9'
                            u'\u231a'
                            u'\u3030'
                            u'\ufe0f'
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u'\U00010000-\U0010ffff'
                            u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
                            u'\U00002702-\U000027B0]+',     
                            re.UNICODE)
        except re.error:
            myre =   re.compile(u'('
                                    u'\ud83c[\udf00-\udfff]|'
                                    u'\ud83d[\udc00-\ude4f]|'
                                    u'\uD83D[\uDE80-\uDEFF]|'
                                    u"(\ud83d[\ude00-\ude4f])|"  # emoticon
                                    u'[\u2600-\u2B55]|'
                                    u'[\u23cf]|'
                                    u'[\u1f918]|'
                                        u'[\u23e9]|'
                                    u'[\u231a]|'
                                    u'[\u3030]|'
                                    u'[\ufe0f]|'
                                    u'\uD83D[\uDE00-\uDE4F]|'
                                    u'\uD83C[\uDDE0-\uDDFF]|'
                                    u'[\u2702-\u27B0]|'
                                    u'\uD83D[\uDC00-\uDDFF])+',
                                    re.UNICODE)
        text=myre.sub('', text)
        return text

if __name__ == "__main__":

    book_marked_url = "https://www.openrice.com/zh/hongkong/explore/chart/most-bookmarked"

    restaurant_review_url = "https://www.openrice.com/zh/hongkong/r-milu-thai-%E0%B8%A1%E0%B8%B4%E0%B8%A5%E0%B8%B9%E0%B9%88%E0%B9%84%E0%B8%97%E0%B8%A2-%E9%8A%85%E9%91%BC%E7%81%A3-%E6%B3%B0%E5%9C%8B%E8%8F%9C-%E6%B5%B7%E9%AE%AE-r588815/reviews"

    # get top 30 restaurant name and its url
    results = Openrice(book_marked_url)
    results.restaurants_name()
    print(results.get_restaurant_data().decode())

    # get target restaurant review
    results = Openrice(restaurant_review_url)
    results.restaurant_review()

    # use json.loads() to convert the string to list 
    print(results.get_restaurant_data().decode())
