# coding=utf-8

from flask import (Flask, render_template, request)
from controller.restaurant_review_data import Openrice, CSV
import json, subprocess, os
from collections import Counter


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

    # get page 1 comments
    restaurant_data = Openrice(path)
    
    restaurant_data.restaurant_review()

    review_list, path = restaurant_data.get_restaurant_data()

    # get page 2 to page 10 comments
    for i in range(0, 9):
    # while True:
        found_path = json.loads(path.decode())

        if len(found_path) != 0:
            restaurant_data = Openrice(found_path[0]["next_page_url"], review_list)
            restaurant_data.restaurant_review()
            review_list, path = restaurant_data.get_restaurant_data()

        else: break

    to_csv_data = CSV(review = review_list,
                    file_path = f"{os.getcwd()}/controller/data/openrice/openrice_sc.csv")
    to_csv_data.to_csv()
    
    subprocess.run(["python", f"{os.getcwd()}/controller/preprocess_data.py"])
    
    subprocess.run(["python", f"{os.getcwd()}/controller/predict_sentiment.py"])
    
    read_csv_data = CSV(review=review_list,
                        file_path=f"{os.getcwd()}/controller/data/openrice/openrice_restaurant_predict_result.csv")

    read_csv_data = json.loads(read_csv_data.read_csv())

    positive_list, negative_list, neutral_list, no_mention_list = \
        find_all_polarity_number(read_csv_data)

    return render_template("result.html", 
                           datas=read_csv_data,
                           index_list=[str(i) for i in range(len(read_csv_data["id"]))],
                           overall_aspect = [sum(item) for item in zip(positive_list, negative_list, neutral_list)],
                           positive_list=positive_list, 
                           negative_list=negative_list,
                           neutral_list=neutral_list,
                           no_mention_list=no_mention_list)


@app.route("/search_list", methods=["POST"])
def search_list():
    restaurant_name = request.form["restaurant_name"]
    label = f" {restaurant_name}"
    return render_template("search_list.html", content=label)


# User Guide
@app.route("/guide")
def user_guide():
    return render_template("guide.html")


def find_all_polarity_number(read_csv_data):

    location_list = list()
    service_list = list()
    price_list = list()
    environment_list = list()
    dish_list = list()
    other_list = list()

    for i in range(len(read_csv_data["id"])):
        location_list.append(read_csv_data["location_traffic_convenience"][str(i)])
        location_list.append(read_csv_data["location_distance_from_business_district"][str(i)])
        location_list.append(read_csv_data["location_easy_to_find"][str(i)])

        service_list.append(read_csv_data["service_wait_time"][str(i)])
        service_list.append(read_csv_data["service_waiters_attitude"][str(i)])
        service_list.append(read_csv_data["service_parking_convenience"][str(i)])
        service_list.append(read_csv_data["service_serving_speed"][str(i)])

        price_list.append(read_csv_data["price_level"][str(i)])
        price_list.append(read_csv_data["price_cost_effective"][str(i)])
        price_list.append(read_csv_data["price_discount"][str(i)])

        dish_list.append(read_csv_data["environment_decoration"][str(i)])
        dish_list.append(read_csv_data["environment_noise"][str(i)])
        dish_list.append(read_csv_data["environment_space"][str(i)])
        dish_list.append(read_csv_data["environment_cleaness"][str(i)])

        environment_list.append(read_csv_data["dish_portion"][str(i)])
        environment_list.append(read_csv_data["dish_taste"][str(i)])
        environment_list.append(read_csv_data["dish_look"][str(i)])
        environment_list.append(read_csv_data["dish_recommendation"][str(i)])

        other_list.append(read_csv_data["others_overall_experience"][str(i)])
        other_list.append(read_csv_data["others_willing_to_consume_again"][str(i)])
    
    location_counter = Counter(location_list)
    service_counter = Counter(service_list)
    price_counter = Counter(price_list)
    dish_counter = Counter(dish_list)
    environment_counter = Counter(environment_list)
    other_counter = Counter(other_list)

    positive = [location_counter[1], service_counter[1], price_counter[1],
                dish_counter[1], environment_counter[1], other_counter[1]]
    
    negative = [location_counter[-1], service_counter[-1], price_counter[-1],
                dish_counter[-1], environment_counter[-1], other_counter[-1]]

    neutral = [location_counter[0], service_counter[0], price_counter[0],
                dish_counter[0], environment_counter[0], other_counter[0]]
    
    no_mention = [location_counter[-2], service_counter[-2], price_counter[-2],
                  dish_counter[-2], environment_counter[-2], other_counter[-2]]

    return positive, negative, neutral, no_mention



if __name__ == "__main__":
    app.run()
