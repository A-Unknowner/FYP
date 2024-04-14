# coding=utf-8

from flask import (Flask, render_template, request)
from controller.restaurant_review_data import Openrice, CSV
import json, subprocess, os
# from collections import Counter
from controller.chart_data import find_all_polarity_number_and_percentage, total_coarse_grain_aspect_percentage, five_star_calculation, each_comment_sub_aspect_polarity
from urllib import parse


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

    restaurant_name, path = request.form["restaurant_name"] , request.form["analyze_bttn"]

    # get page 1 comments
    restaurant_data = Openrice(path)
    
    restaurant_data.restaurant_review()

    review_list, path = restaurant_data.get_restaurant_data()

    # get page 2 to page 10 comments
    for i in range(0, 3):
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

    positive_list, negative_list, neutral_list, no_mention_list, \
    total_positive_percentage, total_negative_percentage, total_neutral_percentage, each_comment_aspect_percentage= \
        find_all_polarity_number_and_percentage(read_csv_data)
    
    total_coarse_grain_aspect_percentage_list = total_coarse_grain_aspect_percentage(positive_list, negative_list, neutral_list)
    
    five_star_list = five_star_calculation(read_csv_data)




    location_traffic_convenience_list, location_distance_from_business_district_list, \
            location_easy_to_find_list, service_wait_time_list, \
            service_waiters_attitude_list, service_parking_convenience_list, \
            service_serving_speed_list, price_level_list, \
            price_cost_effective_list, price_discount_list, \
            environment_decoration_list, environment_noise_list, \
            environment_space_list, environment_cleaness_list, \
            dish_portion_list, dish_taste_list,\
            dish_look_list, dish_recommendation_list,\
            others_overall_experience_list, others_willing_to_consume_again_list = each_comment_sub_aspect_polarity(read_csv_data)

    print("five_star_list", five_star_list)

    return render_template("result.html", 
                        restaurant_name = restaurant_name,
                        datas=read_csv_data,
                        index_list=[str(i) for i in range(len(read_csv_data["id"]))],
                        overall_positive = sum(positive_list),
                        overall_negative = sum(negative_list),
                        overall_neutral = sum(neutral_list),
                        overall_aspect = [sum(item) for item in zip(positive_list, negative_list, neutral_list)],
                        positive_list=positive_list, 
                        negative_list=negative_list,
                        neutral_list=neutral_list,
                        no_mention_list=no_mention_list,

                        id_length = len(read_csv_data["id"]),


                        # each sub aspects polarity list
                        location_traffic_convenience_list = location_traffic_convenience_list,
                        location_distance_from_business_district_list = location_distance_from_business_district_list, 
                        location_easy_to_find_list = location_easy_to_find_list, 

                        service_wait_time_list = service_wait_time_list, 
                        service_waiters_attitude_list = service_waiters_attitude_list, 
                        service_parking_convenience_list = service_parking_convenience_list, 
                        service_serving_speed_list = service_serving_speed_list, 

                        price_level_list = price_level_list, 
                        price_cost_effective_list = price_cost_effective_list, 
                        price_discount_list = price_discount_list, 

                        environment_decoration_list = environment_decoration_list, 
                        environment_noise_list = environment_noise_list, 
                        environment_space_list = environment_space_list, 
                        environment_cleaness_list = environment_cleaness_list, 

                        dish_portion_list = dish_portion_list, 
                        dish_taste_list = dish_taste_list,
                        dish_look_list = dish_look_list, 
                        dish_recommendation_list = dish_recommendation_list,

                        others_overall_experience_list = others_overall_experience_list, 
                        others_willing_to_consume_again_list = others_willing_to_consume_again_list,

                        # each aspects total percent list
                        each_aspects_total_percent_list = total_coarse_grain_aspect_percentage_list,

                        # this list is stored the 5 stars values
                        five_star_list = five_star_list,

                        # total percentage
                        total_positive_percentage = total_positive_percentage, 
                        total_negative_percentage = total_negative_percentage, 
                        total_neutral_percentage = total_neutral_percentage, 
                        each_comment_percentage = each_comment_aspect_percentage)
    

@app.route("/search_list", methods=["POST"])
def search_list():
    restaurant_name = parse.quote_plus(request.form["restaurant_name"])
    # search_link = f"http://www.openrice.com/chinese/restaurant/sr1.htm?inputstrwhat={restaurant_name}"
    search_link = f"http://www.openrice.com/english/restaurant/sr1.htm?inputstrwhat={restaurant_name}"

    results = Openrice(search_link)
    results.search_restaurant()

    restaurant_info, path = results.get_restaurant_data()
    res = json.loads(restaurant_info.decode())
    # print(res)
    return render_template("search_list.html", datas=res, key=restaurant_name)


# User Guide
@app.route("/guide")
def user_guide():
    return render_template("guide.html")


if __name__ == "__main__":
    app.run()
