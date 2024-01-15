from collections import Counter



def find_specific_aspect_polarity(read_csv_data):

    # location
    location_traffic_convenience = list()
    location_distance_from_business_district = list()
    location_easy_to_find = list()

    # service
    service_wait_time = list()
    service_waiters_attitude = list()
    service_parking_convenience = list()
    service_serving_speed = list()

    # price
    price_level = list()
    price_cost_effective = list()
    price_discount = list()

    # environment
    environment_decoration = list()
    environment_noise = list()
    environment_space = list()
    environment_cleaness = list()

    # dish
    dish_portion = list()
    dish_taste = list()
    dish_look = list()
    dish_recommendation = list()

    # others
    others_overall_experience = list()
    others_willing_to_consume_again = list()

    for i in range(len(read_csv_data["id"])):

        # location
        location_traffic_convenience.append(read_csv_data["location_traffic_convenience"][str(i)])
        location_distance_from_business_district.append(read_csv_data["location_distance_from_business_district"][str(i)])
        location_easy_to_find.append(read_csv_data["location_easy_to_find"][str(i)])

        # service
        service_wait_time.append(read_csv_data["service_wait_time"][str(i)])
        service_waiters_attitude.append(read_csv_data["service_waiters_attitude"][str(i)])
        service_parking_convenience.append(read_csv_data["service_parking_convenience"][str(i)])
        service_serving_speed.append(read_csv_data["service_serving_speed"][str(i)])

        # price
        price_level.append(read_csv_data["price_level"][str(i)])
        price_cost_effective.append(read_csv_data["price_cost_effective"][str(i)])
        price_discount.append(read_csv_data["price_discount"][str(i)])

        # environment
        environment_decoration.append(read_csv_data["environment_decoration"][str(i)])
        environment_noise.append(read_csv_data["environment_noise"][str(i)])
        environment_space.append(read_csv_data["environment_space"][str(i)])
        environment_cleaness.append(read_csv_data["environment_cleaness"][str(i)])

        # dish
        dish_portion.append(read_csv_data["dish_portion"][str(i)])
        dish_taste.append(read_csv_data["dish_taste"][str(i)])
        dish_look.append(read_csv_data["dish_look"][str(i)])
        dish_recommendation.append(read_csv_data["dish_recommendation"][str(i)])

        # others
        others_overall_experience.append(read_csv_data["others_overall_experience"][str(i)])
        others_willing_to_consume_again.append(read_csv_data["others_willing_to_consume_again"][str(i)])
    
    
    # location
    location_list = [{"location_traffic_convenience":Counter(location_traffic_convenience),
                      "location_distance_from_business_district":Counter(location_distance_from_business_district),
                      "location_easy_to_find":Counter(location_easy_to_find)}]
    
    # service
    service_list = {"service_wait_time":Counter(service_wait_time),
                    "service_waiters_attitude":Counter(service_waiters_attitude),
                    "service_parking_convenience":Counter(service_parking_convenience),
                    "service_serving_speed":Counter(service_serving_speed)}

    # price
    price_list = {"price_level":Counter(price_level),
                  "price_cost_effective":Counter(price_cost_effective),
                  "price_discount":Counter(price_discount)}

    # environment
    environment_list = {"environment_decoration":Counter(environment_decoration),
                        "environment_noise":Counter(environment_noise),
                        "environment_space":Counter(environment_space),
                        "environment_cleaness":Counter(environment_cleaness)}

    # dish
    dish_list = {"dish_portion":Counter(dish_portion),
                 "dish_taste":Counter(dish_taste),
                 "dish_look":Counter(dish_look),
                 "dish_recommendation":Counter(dish_recommendation)}

    # others
    others_list = {"others_overall_experience":Counter(others_overall_experience),
                 "others_willing_to_consume_again":Counter(others_willing_to_consume_again)}

    return location_list, service_list, price_list, environment_list, dish_list, others_list

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

    return positive, negative, neutral, no_mention, location_counter