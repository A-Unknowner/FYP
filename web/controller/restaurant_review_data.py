# coding=utf-8
from urllib import parse

import lxml.html
from bs4 import BeautifulSoup
from lxml import etree
import requests, json, re, os
from langdetect import detect
from opencc import OpenCC

import pandas as pd

# import numpy as np

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})


class Openrice:

    def __init__(self, url, review=None):

        if review != None:
            self.__restaurant_data = json.loads(review.decode())
        else:
            self.__restaurant_data = list()
        self.__next_page_path = list()

        if "http" not in url:
            self.__url = f"https://www.openrice.com{url}/reviews"
        else:
            self.__url = url

        self.__page = requests.get(self.__url, headers=headers)
        self.__soup = BeautifulSoup(self.__page.content, "html.parser")
        self.__dom = etree.HTML(str(self.__soup))

    # get 30 most popular restaurant name and its page url
    def restaurants_name(self):

        link_elements = self.__dom.xpath('//div[@class="poi-chart-main-grid-item-deskop-title-row-left-section"]')

        for element in link_elements:
            name = element.xpath(".//text()")[0].replace("\n", "").strip()
            details = "".join(element.xpath(".//text()")[1::]).replace("\n", "").strip()
            href = element.xpath(".//@href")[0]
            location = element.xpath(".//@href")
            image = element.xpath('.//@src')[0]

            # print(len(location))

            self.__restaurant_data.append(
                {"restaurant_name": name,
                 "restaurant_details": details,
                 "restaurant_img_url": image,
                 #  "restaurant_url" : f"https://www.openrice.com{href}/reviews"}
                 "restaurant_url": href}
            )


    def restaurant_review(self):
        converter = OpenCC("s2hk.json")
        # review_user = self.__dom.xpath('//div[@itemprop="author"]')
        comments = self.__dom.xpath('//section[@class="review-container"]')
        # comments = self.__dom.xpath('//div[@itemprop="description"]')
        num_of_page = self.__dom.xpath('//*[@id="sr2-review-container"]/div[3]/div/a')
        # print("comment", comments)

        if len(self.__restaurant_data) == 0:
            for i in range(len(comments)):

                # username = review_user[i].xpath(".//text()")[1].strip()
                # user_review = comments[i].xpath(".//text()")[0]
                # user_review = ''.join([com if not com in ["\n", "\r"] and not com.isdigit() and not "留言" in com and not "讚好" in com and not "瀏覽" in com else "" for com in comments[i].xpath("//section[@class='review-container']")[0].xpath(".//text()")]).replace("\r\n\r\n","")
                user_review = ''.join([com if not com in ["\n",
                                                          "\r"] and not com.isdigit() and not "留言" in com and not "讚好" in com and not "瀏覽" in com else ""
                                                        #   "\r"] and not com.isdigit() and not "comments" in com and not "likes" in com and not "views" in com else ""
                                       for com in comments[i].xpath(".//text()")]).replace("                    ", "")
                # print("review", comments[i].xpath("//section[@class='review-container']")[0].xpath(".//text()"))
                # print("review", ''.join([com if not com in ["\n", "\r"] and not com.isdigit() and not "留言" in com and not "讚好" in com and not "瀏覽" in com else "" for com in comments[i].xpath("//section[@class='review-container']")[0].xpath(".//text()")]).replace("\r\n\r\n",""))
                # print("review", comments[i].xpath(".//text()"))
                user_review = user_review.replace("\r\n", "").strip()
                # user_review = self.emoji_filter(user_review)
                # print("review", user_review)

                if detect(user_review) != "en":
                    self.__restaurant_data.append(
                        # {"username" : username,
                        {"id": i,
                         # translate data from cantonese to simplify chinese
                         "user_review": converter.convert(user_review)}
                    )
        else:
            start = self.__restaurant_data[-1]["id"] + 1
            for i in range(len(comments)):

                # username = review_user[i].xpath(".//text()")[1].strip()
                # user_review = comments[i].xpath(".//text()")[1]
                user_review = ''.join([com if not com in ["\n",
                                                          "\r"] and not com.isdigit() and not "留言" in com and not "讚好" in com and not "瀏覽" in com else ""
                                                        #   "\r"] and not com.isdigit() and not "comments" in com and not "likes" in com and not "views" in com else ""
                                       for com in comments[i].xpath(".//text()")]).replace("                    ", "")
                # print("review", comments[i].xpath(".//text()"))
                # print("review", comments[i].xpath(".//text()"))

                user_review = user_review.replace("\r\n", "").strip()
                # user_review = self.emoji_filter(user_review)
                # print("review", user_review)
                if detect(user_review) != "en":
                    self.__restaurant_data.append(
                        # {"username" : username,
                        {"id": start + i,
                         # translate data from cantonese to simplify chinese
                         "user_review": converter.convert(user_review)}
                    )

        # print('num_of_page[-1].xpath(".//@class")', num_of_page[-1].xpath(".//@class"))
        next_button_class = num_of_page[-1].xpath(".//@class")[0]
        # print('num_of_page[-1].xpath(".//@href")', num_of_page[-1].xpath(".//@href"))
        next_page_path = num_of_page[-1].xpath(".//@href")

        if (next_button_class == "pagination-button next js-next" and
                len(next_page_path) != 0):
            self.__next_page_path.append({"next_page_url": f"https://www.openrice.com{next_page_path[0]}"})

    def search_restaurant(self):
        if self.__soup.title.string != "Verification":
            # print(self.__soup.title.string)
            elements = self.__soup.find_all("section", class_="poi-list-cell-wrapper")
            for element in elements:
                name = element.find_all_next("a", class_="poi-name poi-list-cell-link")[0]
                address = element.find_all_next("div", class_="poi-list-cell-line-info")[0]
                image = element.find_all_next("div", class_="rms-photo")[0]
                self.__restaurant_data.append(
                    {
                        "restaurant_name": name.text.strip(),
                         "restaurant_img_url": image["style"].replace('background-image:url(', '').replace(');', ''),
                         "restaurant_address": address.text.strip().replace(" ", "").split("\n\n")[0],
                         "restaurant_details": address.text.strip().replace(" ", "").split("\n\n")[1].replace("\n", " "),
                         "restaurant_url": f"https://www.openrice.com/{name['href']}/reviews"}
                )
        else:
            print("Error: search_restaurant(): No results found.")

    def get_restaurant_data(self):
        return json.dumps(self.__restaurant_data, ensure_ascii=False).encode('utf8'), \
            json.dumps(self.__next_page_path, ensure_ascii=False).encode('utf8')

    # def get_restaurant_address(self):
    #     xpath = '//a[@data-href="#map"]'
    #     chinese_address = self.__dom.xpath(xpath)[0].text.replace("\n", "").strip()
    #     english_address = self.__dom.xpath(xpath)[1].text.replace("\n", "").strip()
    #
    #     return json.dumps(chinese_address, ensure_ascii=False).encode('utf8'), \
    #            json.dumps(english_address, ensure_ascii=False).encode('utf8')

    def restaurant_info(self):
        xpath = '//div[@class="photo"]'
        image = self.__dom.xpath(xpath)[0]
        for item in image.items():
            if item[0] == "style":
                restaurant_img_url = item[1].replace('background-image: url(', '')[:-1]
                break
        xpath = '//a[@data-href="#map"]'
        chinese_address = self.__dom.xpath(xpath)[0].text.replace("\n", "").strip()
        english_address = self.__dom.xpath(xpath)[1].text.replace("\n", "").strip()
        xpath = '//div[@class="content js-text-wrapper"]'
        transport_section = self.__dom.xpath(xpath)[0].text.replace("\n", "").strip()
        xpath = '//div[@class="left-col-content-section left-middle-col-section"]//div[@class="content"]'
        telephone = self.__dom.xpath(xpath)[0].text.replace("\n", "").strip() if len(self.__dom.xpath(xpath)) > 0 else "N/A"
        # xpath = '//div[@class="content js-text-wrapper"]'
        # introduction_section = self.__dom.xpath(xpath)[1].text.replace("\n", "").strip()
        today_opening_hours = str()
        opening_hours = list()
        xpath = '//div[@class="opening-hours-day"]'
        elements = self.__dom.xpath(xpath)
        for element_index in range(len(elements)):
            if element_index == 0:
                today_opening_hours = elements[element_index].xpath('.//div[@class="opening-hours-time"]//div')[0].text.strip()
            else:
                opening_hours.append(
                    {
                        "date": elements[element_index].xpath('.//div[@class="opening-hours-date "]')[0].text.strip() if len(elements[element_index].xpath('.//div[@class="opening-hours-date "]')) > 0 else elements[element_index].xpath('.//div[@class="opening-hours-date"]')[0].text.strip(),
                        "time": elements[element_index].xpath('.//div[@class="opening-hours-time"]//div')[0].text.strip()
                    }
                )
        xpath = '//div[@class="or-section-expandable collapse"]//section'
        elements = self.__dom.xpath(xpath)
        payment = list()
        seats_num = int()
        other_service = list()
        for element in elements:
            if element.xpath('.//div[@class="title"]')[0].text.strip() == "付款方式":
                for tags in element.xpath('.//div[@class="comma-tags"]//span'):
                    payment.append(tags.text.strip())
            elif element.xpath('.//div[@class="title"]')[0].text.strip() == "座位數目":
                seats_num = int(element.xpath('.//div[@class="content"]')[0].text.strip())
            elif element.xpath('.//div[@class="title"]')[0].text.strip() == "其他資料":
                for tags in element.xpath('.//div//div[@class="condition-item"]'):
                    if tags.xpath('.//span')[0].attrib['class'] == 'or-sprite-inline-block d_sr2_lhs_tick_desktop':
                        other_service.append(
                            {
                                "had": True,
                                "tags": tags.xpath('.//span[@class="condition-name"]')[0].text.strip()
                            }
                        )
                    elif tags.xpath('.//span')[0].attrib['class'] == 'or-sprite-inline-block d_sr2_lhs_cross_desktop':
                        other_service.append(
                            {
                                "had": False,
                                "tags": tags.xpath('.//span[@class="condition-name"]')[0].text.strip(),
                            }
                        )
        self.__restaurant_data.append(
            {
                "restaurant_img_url": restaurant_img_url,
                "chinese_address": chinese_address,
                "english_address": english_address,
                "transport_section": transport_section,
                "telephone": telephone,
                # "introduction_section": introduction_section,
                "today_opening_hours": today_opening_hours,
                "opening_hours": opening_hours,
                "payment": payment,
                "seats_num": seats_num,
                "other_service": other_service
            }
        )


class CSV:
    def __init__(self, review, file_path):
        # json data
        # self.review = review

        self.review = json.loads(review.decode())

        self.__file_path = file_path

    def to_csv(self):
        # store original cantonese data and simplify chinese data to openrice_sc.csv
        # data_file_path = "./data/openrice/openrice_sc.csv"

        if os.path.isfile(self.__file_path):
            os.remove(self.__file_path)

        dict = {"id": [str(i) for i in range(0, len(self.review))],
                "content": [f'\"{self.review[i]["user_review"]}\"' for i in range(0, len(self.review))],
                "location_traffic_convenience": int(),
                "location_distance_from_business_district": int(),
                "location_easy_to_find": int(),
                "service_wait_time": int(),
                "service_waiters_attitude": int(),
                "service_parking_convenience": int(),
                "service_serving_speed": int(),
                "price_level": int(),
                "price_cost_effective": int(),
                "price_discount": int(),
                "environment_decoration": int(),
                "environment_noise": int(),
                "environment_space": int(),
                "environment_cleaness": int(),
                "dish_portion": int(),
                "dish_taste": int(),
                "dish_look": int(),
                "dish_recommendation": int(),
                "others_overall_experience": int(),
                "others_willing_to_consume_again": int()}
        df = pd.DataFrame(dict).astype({"location_traffic_convenience": 'Int64'})

        df.to_csv(self.__file_path, encoding="utf_8_sig", index=False)

    def read_csv(self):
        # converter = OpenCC("s2hk.json")

        data_list = [data["user_review"] for data in self.review]

        # data_list = [converter.convert(data["user_review"]) for data in self.review]

        df_datas = pd.read_csv(self.__file_path)

        df_datas["content"] = data_list

        return df_datas.to_json(force_ascii=False)


if __name__ == "__main__":
    # book_marked_url = "https://www.openrice.com/zh/hongkong/explore/chart/most-bookmarked"

    # restaurant_review_url = "https://www.openrice.com/zh/hongkong/r-milu-thai-%E0%B8%A1%E0%B8%B4%E0%B8%A5%E0%B8%B9%E0%B9%88%E0%B9%84%E0%B8%97%E0%B8%A2-%E9%8A%85%E9%91%BC%E7%81%A3-%E6%B3%B0%E5%9C%8B%E8%8F%9C-%E6%B5%B7%E9%AE%AE-r588815/reviews"
    restaurant_review_url = "https://www.openrice.com/zh/hongkong/r-milu-thai-%E0%B8%A1%E0%B8%B4%E0%B8%A5%E0%B8%B9%E0%B9%88%E0%B9%84%E0%B8%97%E0%B8%A2-%E9%8A%85%E9%91%BC%E7%81%A3-%E6%B3%B0%E5%9C%8B%E8%8F%9C-%E6%B5%B7%E9%AE%AE-r588815"

    # # get top 30 restaurant name and its url
    # results = Openrice(book_marked_url)
    # results.restaurants_name()
    # restaurant_info, path = results.get_restaurant_data()

    # # print(restaurant_info.decode())
    # # print(path.decode())

    # get target restaurant review
    results = Openrice(restaurant_review_url)
    results.restaurant_info()
    reviews_info, path = results.get_restaurant_data()
    print(reviews_info.decode())

    # CSV(reviews_info).to_csv()

    # restaurant_name = "MoMo"
    # search_link = f"http://www.openrice.com/chinese/restaurant/sr1.htm?inputstrwhat={restaurant_name}"
    # results = Openrice(search_link)
    # results.search_restaurant()
    # restaurant_info, path = results.get_restaurant_data()
    #
    # print(restaurant_info.decode())

    # print(reviews_info.decode())
    # print(path.decode())
    # use json.loads() to convert the string to list
    # print(results.get_restaurant_data().decode())
