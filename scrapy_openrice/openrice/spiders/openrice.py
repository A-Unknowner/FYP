from typing import Any
from scrapy.http import Response
from openrice.items import OpenriceItem
import scrapy
import re
# import time

class OpenRiceSpider(scrapy.Spider):

    name = "openrice"

    allowed_domains = ["openrice.com"]

    start_urls = ["https://www.openrice.com/zh/hongkong/explore/chart/most-bookmarked"]

    def parse(self, response):

        link_elements = response.xpath('//div[@class="poi-chart-main-grid-item-deskop-title-row-left-section-poi-info-name"]')

        for element in link_elements:

            # name = element.xpath(".//text()").extract_first()
            href = element.xpath(".//@href").extract_first()

            # item = OpenriceItem()
            # item["restaurant_name"] = name.replace("\n", "").strip()
            # item["restaurant_url"] = f"https://www.openrice.com{href}/reviews"

        yield scrapy.Request(f"https://www.openrice.com{href}/reviews", self.parse_detail)

        
    def parse_detail(self, response):

        # rest_name = response.xpath('//*[@id="global-container"]/main/div[2]/div[1]/div[2]/section/div[2]/div[2]/div[1]/div[1]/h1/span[1]/text()')
        comments = response.xpath('//div[@itemprop="description"]')
        num_of_page = response.xpath('//*[@id="sr2-review-container"]/div[3]/div/a')

        for comment in comments:

            user_review = comment.xpath(".//text()").extract_first()

            item = OpenriceItem(
                # restaurant_name = rest_name.extract_first().strip(),

                user_review = self.emoji_filter(user_review.replace("\r\n", "").strip())
            )

            yield item

        next_button_class = num_of_page[-1].xpath(".//@class").extract_first().strip()

        next_page_path = num_of_page[-1].xpath(".//@href").extract_first()

        if next_button_class == "pagination-button next js-next":
            yield scrapy.Request(url = f"https://www.openrice.com{next_page_path}", callback=self.parse_detail)

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

