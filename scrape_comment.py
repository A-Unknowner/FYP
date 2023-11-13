import requests
from bs4 import BeautifulSoup
url = "https://www.openrice.com/zh/hongkong/r-%E4%B9%9D%E4%BB%BD%E9%A3%BD-%E7%B4%85%E7%A3%A1-%E5%8F%B0%E7%81%A3%E8%8F%9C-r818839/reviews"

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("div", {"itemprop":"description"})
comment_list = list()
for result in results:
    comment_list.append(result.text.replace("\n更多", "").strip().split("\r\n")[0])

print(f"Collected comments: {len(comment_list)}")
for i in comment_list:
    print(i, end="\n\n")
