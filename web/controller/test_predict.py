# coding=utf-8

from flask import Flask, jsonify
from restaurant_review_data import Openrice, CSV

import subprocess

if __name__ == "__main__":

    book_marked_url = "https://www.openrice.com/zh/hongkong/explore/chart/most-bookmarked"

    # get top 30 restaurant name and its url
    restaurant_data = Openrice(book_marked_url)

    restaurant_data.restaurants_name()

    restaurant_list, path = restaurant_data.get_restaurant_data()

    print(f"\n{restaurant_list.decode()}\n")
    

    hardcode_url = "https://www.openrice.com/zh/hongkong/r-milu-thai-%E0%B8%A1%E0%B8%B4%E0%B8%A5%E0%B8%B9%E0%B9%88%E0%B9%84%E0%B8%97%E0%B8%A2-%E9%8A%85%E9%91%BC%E7%81%A3-%E6%B3%B0%E5%9C%8B%E8%8F%9C-%E6%B5%B7%E9%AE%AE-r588815/reviews"

    restaurant_data = Openrice(hardcode_url)

    restaurant_data.restaurant_review()

    review_list, path = restaurant_data.get_restaurant_data()

    print(f"\n{review_list.decode()}\n")


    to_csv_data = CSV(review = review_list, 
                    file_path = "./data/openrice/openrice_sc.csv")
    to_csv_data.to_csv()


    subprocess.run(["python", "preprocess_data.py"])

    subprocess.run(["python", "predict_sentiment.py"])
    
    
    read_csv_data = CSV(review = review_list, 
                        file_path = "./data/openrice/openrice_restaurant_predict_result.csv")

    print(read_csv_data.read_csv())


