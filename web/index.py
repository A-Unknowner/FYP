# coding=utf-8

from flask import (Flask, render_template, request)
from controller.restaurant_review_data import Openrice, CSV
import json
import subprocess

app = Flask(__name__)


# testing

@app.route("/")
def index():

    book_marked_url = "https://www.openrice.com/zh/hongkong/explore/chart/most-bookmarked"

    # get top 30 restaurant name and its url
    restaurant_data = Openrice(book_marked_url)

    restaurant_data.restaurants_name()

    restaurant_list, path = restaurant_data.get_restaurant_data()
    restaurants = restaurant_list.decode()
    results_json = json.loads(restaurants)

    return render_template("index.html", datas=results_json)


@app.route('/result', methods=['POST'])
def analyze_review():

    path = request.form["analyze_bttn"]
    print(path)

    restaurant_data = Openrice(path)
    
    restaurant_data.restaurant_review()

    review_list, path = restaurant_data.get_restaurant_data()

    print(f"\n{review_list.decode()}\n")

    to_csv_data = CSV(review = review_list,
                    file_path = "./data/openrice/openrice_sc.csv")
    to_csv_data.to_csv()
    
    subprocess.run(["python", "preprocess_data.py"])
    
    subprocess.run(["python", "predict_sentiment.py"])
    
    read_csv_data = CSV(review=review_list,
                        file_path="./data/openrice/openrice_restaurant_predict_result.csv")

    return render_template("result.html", datas=read_csv_data.read_csv())


@app.route("/search_list", methods=["POST"])
def search_list():
    restaurant_name = request.form["restaurant_name"]
    label = f" {restaurant_name}"
    return render_template("search_list.html", content=label)


# User Guide
@app.route("/guide")
def user_guide():
    return render_template("guide.html")


if __name__ == "__main__":
    app.run()
