# coding=utf-8

from collections import Counter

def find_all_polarity_number_and_percentage(read_csv_data):

    location_list = list()
    service_list = list()
    price_list = list()
    environment_list = list()
    dish_list = list()
    other_list = list()

    each_comment_aspect_percent = list()

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

        environment_list.append(read_csv_data["environment_decoration"][str(i)])
        environment_list.append(read_csv_data["environment_noise"][str(i)])
        environment_list.append(read_csv_data["environment_space"][str(i)])
        environment_list.append(read_csv_data["environment_cleaness"][str(i)])

        dish_list.append(read_csv_data["dish_portion"][str(i)])
        dish_list.append(read_csv_data["dish_taste"][str(i)])
        dish_list.append(read_csv_data["dish_look"][str(i)])
        dish_list.append(read_csv_data["dish_recommendation"][str(i)])


        other_list.append(read_csv_data["others_overall_experience"][str(i)])
        other_list.append(read_csv_data["others_willing_to_consume_again"][str(i)])


        each_comment_aspect_percent.append(each_aspects_percentage(location_list, service_list, price_list, environment_list, dish_list, other_list))
                                                                    

    location_counter, service_counter, price_counter, environment_counter, dish_counter, other_counter = \
        get_aspects_counter(location_list, service_list, price_list, environment_list, dish_list, other_list)

    total_list = location_list + service_list + price_list + dish_list + environment_list + other_list

    total_positive_percentage, total_negative_percentage, total_neutral_percentage = total_percentage(location_list, 
                                                                                                      service_list, 
                                                                                                      price_list,
                                                                                                      dish_list, 
                                                                                                      environment_list, 
                                                                                                      other_list, 
                                                                                                      total_list)

    positive = [location_counter[1], service_counter[1], price_counter[1],
                dish_counter[1], environment_counter[1], other_counter[1]]
    
    negative = [location_counter[-1], service_counter[-1], price_counter[-1],
                dish_counter[-1], environment_counter[-1], other_counter[-1]]

    neutral = [location_counter[0], service_counter[0], price_counter[0],
                dish_counter[0], environment_counter[0], other_counter[0]]
    
    no_mention = [location_counter[-2], service_counter[-2], price_counter[-2],
                  dish_counter[-2], environment_counter[-2], other_counter[-2]]
    
    return positive, negative, neutral, no_mention, total_positive_percentage, total_negative_percentage, total_neutral_percentage, each_comment_aspect_percent


def total_percentage(location_list, service_list, price_list, dish_list, environment_list, other_list, total_list):

    location_total, service_total, price_total, dish_total, environment_total, other_total = \
        filter_not_mentioned(location_list, service_list, price_list, dish_list, environment_list, other_list)

    total_list_counter = Counter(total_list)

    total_polarities = location_total + service_total + price_total + dish_total + environment_total + other_total

    positive_percentage = calculate(total_list_counter[1], total_polarities)

    negative_percentage = calculate(total_list_counter[-1], total_polarities)

    neutral_percentage = calculate(total_list_counter[0], total_polarities)

    return positive_percentage, negative_percentage, neutral_percentage

def total_coarse_grain_aspect_percentage(positive_list, negative_list, neutral_list):

    location_total_num, service_total_num, price_total_num, environment_total_num, dish_total_num, others_total_num = \
        [sum(item) for item in zip(positive_list, negative_list, neutral_list)]

    location_positive_num, service_positive_num, price_positive_num, environment_positive_num, dish_positive_num, others_positive_num = \
        positive_list
    
    location_negative_num, service_negative_num, price_negative_num, environment_negative_num, dish_negative_num, others_negative_num = \
        negative_list 

    location_neutral_num, service_neutral_num, price_neutral_num, environment_neutral_num, dish_neutral_num, others_neutral_num = \
        neutral_list 
    
    location_positive_percent,  location_negative_percent,  location_neutral_percent = \
                                (calculate(location_positive_num, location_total_num), 
                                 calculate(location_negative_num, location_total_num), 
                                 calculate(location_neutral_num, location_total_num))

    service_positive_percent,  service_negative_percent,  service_neutral_percent = \
                                (calculate(service_positive_num, service_total_num), 
                                 calculate(service_negative_num, service_total_num), 
                                 calculate(service_neutral_num, service_total_num))

    price_positive_percent,  price_negative_percent,  price_neutral_percent = \
                                (calculate(price_positive_num, price_total_num), 
                                 calculate(price_negative_num, price_total_num), 
                                 calculate(price_neutral_num, price_total_num))
    
    environment_positive_percent,  environment_negative_percent,  environment_neutral_percent = \
                                (calculate(environment_positive_num, environment_total_num), 
                                 calculate(environment_negative_num, environment_total_num), 
                                 calculate(environment_neutral_num, environment_total_num))
    
    dish_positive_percent,  dish_negative_percent,  dish_neutral_percent = \
                                (calculate(dish_positive_num, dish_total_num), 
                                 calculate(dish_negative_num, dish_total_num), 
                                 calculate(dish_neutral_num, dish_total_num))
    
    others_positive_percent,  others_negative_percent,  others_neutral_percent = \
                                (calculate(others_positive_num, others_total_num), 
                                 calculate(others_negative_num, others_total_num), 
                                 calculate(others_neutral_num, others_total_num))


    return [

        {"total_location_positive_percent" : location_positive_percent,  
         "total_location_negative_percent" : location_negative_percent,  
         "total_location_neutral_percent" : location_neutral_percent,
         "location_positive" : location_positive_num,
         "location_negative" : location_negative_num,
         "location_neutral" : location_neutral_num},

        {"total_service_positive_percent" : service_positive_percent,  
         "total_service_negative_percent" : service_negative_percent,  
         "total_service_neutral_percent" : service_neutral_percent,
         "service_positive" : service_positive_num,
         "service_negative" : service_negative_num,
         "service_neutral" : service_neutral_num},

        {"total_price_positive_percent" : price_positive_percent,  
         "total_price_negative_percent" : price_negative_percent,  
         "total_price_neutral_percent" : price_neutral_percent,
         "price_positive" : price_positive_num,
         "price_negative" : price_negative_num,
         "price_neutral" : price_neutral_num},

        {"total_environment_positive_percent" : environment_positive_percent,  
         "total_environment_negative_percent" : environment_negative_percent,  
         "total_environment_neutral_percent" : environment_neutral_percent,
         "environment_positive" : environment_positive_num,
         "environment_negative" : environment_negative_num,
         "environment_neutral" : environment_neutral_num},

        {"total_dish_positive_percent" : dish_positive_percent,  
         "total_dish_negative_percent" : dish_negative_percent,  
         "total_dish_neutral_percent" : dish_neutral_percent,
         "dish_positive" : dish_positive_num,
         "dish_negative" : dish_negative_num,
         "dish_neutral" : dish_neutral_num},

        {"total_others_positive_percent" : others_positive_percent, 
         "total_others_negative_percent" : others_negative_percent, 
         "total_others_neutral_percent" : others_neutral_percent,
         "others_positive" : others_positive_num,
         "others_negative" : others_negative_num,
         "others_neutral" : others_neutral_num},

    ]


def get_aspects_counter(location_list, service_list, price_list, environment_list, dish_list, other_list):

    return Counter(location_list), Counter(service_list), Counter(price_list), \
           Counter(environment_list), Counter(dish_list), Counter(other_list)

def calculate(value, total_value):

    try:

        results = (value / total_value) * 100
        # print(results)
        return round(results, 1)
    
    except ZeroDivisionError:

        return 0
    
    
def filter_not_mentioned(location_list, service_list, price_list, dish_list, environment_list, other_list):

    location_total = len(list(filter(lambda x: x != -2, location_list)))
    service_total = len(list(filter(lambda x: x != -2, service_list)))
    price_total = len(list(filter(lambda x: x != -2, price_list)))
    dish_total = len(list(filter(lambda x: x != -2, dish_list)))
    environment_total = len(list(filter(lambda x: x != -2, environment_list)))
    other_total = len(list(filter(lambda x: x != -2, other_list)))

    return location_total, service_total, price_total, dish_total, environment_total, other_total

def each_aspects_percentage(location_list, service_list, price_list, environment_list, dish_list, other_list):

    location_counter, service_counter, price_counter, environment_counter, dish_counter, other_counter = \
        get_aspects_counter(location_list, service_list, price_list, environment_list, dish_list, other_list)
    
    location_total, service_total, price_total, dish_total, environment_total, other_total = \
        filter_not_mentioned(location_list, service_list, price_list, dish_list, environment_list, other_list)
    
    location_percentage = {"positive_percent" : calculate(location_counter[1], location_total), 
                           "negative_percent" : calculate(location_counter[-1], location_total), 
                           "neutral_percent" : calculate(location_counter[0], location_total)}
    
    service_percentage = {"positive_percent" : calculate(service_counter[1], service_total), 
                           "negative_percent" : calculate(service_counter[-1], service_total), 
                           "neutral_percent" : calculate(service_counter[0], service_total)}

    price_percentage = {"positive_percent" : calculate(price_counter[1], price_total), 
                           "negative_percent" : calculate(price_counter[-1], price_total), 
                           "neutral_percent" : calculate(price_counter[0], price_total)}
    
    environment_percentage = {"positive_percent" : calculate(environment_counter[1], environment_total), 
                           "negative_percent" : calculate(environment_counter[-1], environment_total), 
                           "neutral_percent" : calculate(environment_counter[0], environment_total)}
    
    dish_percentage = {"positive_percent" : calculate(dish_counter[1], dish_total), 
                           "negative_percent" : calculate(dish_counter[-1], dish_total), 
                           "neutral_percent" : calculate(dish_counter[0], dish_total)}
    
    other_percentage = {"positive_percent" : calculate(other_counter[1], other_total), 
                        "negative_percent" : calculate(other_counter[-1], other_total), 
                        "neutral_percent" : calculate(other_counter[0], other_total)}

    return [{"location_percentage" : location_percentage}, {"service_percentage" : service_percentage}, 
            {"price_percentage" : price_percentage}, {"environment_percentage" : environment_percentage}, 
            {"dish_percentage" : dish_percentage}, {"other_percentage" : other_percentage}]


def each_comment_polarity(read_csv_data):

    each_comment_polarity = list()

    for i in range(len(read_csv_data["id"])):
        each_review_data = [
            read_csv_data["location_traffic_convenience"][str(i)],
            read_csv_data["location_distance_from_business_district"][str(i)],
            read_csv_data["location_easy_to_find"][str(i)],

            read_csv_data["service_wait_time"][str(i)],
            read_csv_data["service_waiters_attitude"][str(i)],
            read_csv_data["service_parking_convenience"][str(i)],
            read_csv_data["service_serving_speed"][str(i)],

            read_csv_data["price_level"][str(i)],
            read_csv_data["price_cost_effective"][str(i)],
            read_csv_data["price_discount"][str(i)],

            read_csv_data["environment_decoration"][str(i)],
            read_csv_data["environment_noise"][str(i)],
            read_csv_data["environment_space"][str(i)],
            read_csv_data["environment_cleaness"][str(i)],

            read_csv_data["dish_portion"][str(i)],
            read_csv_data["dish_taste"][str(i)],
            read_csv_data["dish_look"][str(i)],
            read_csv_data["dish_recommendation"][str(i)],

            read_csv_data["others_overall_experience"][str(i)],
            read_csv_data["others_willing_to_consume_again"][str(i)]
        ]
        

        each_comment_polarity.append(each_review_data)

    return each_comment_polarity

def each_comment_sub_aspect_polarity(read_csv_data):

    location_traffic_convenience_list = list()
    location_distance_from_business_district_list = list()
    location_easy_to_find_list = list()

    service_wait_time_list = list()
    service_waiters_attitude_list = list()
    service_parking_convenience_list = list()
    service_serving_speed_list = list()

    price_level_list = list()
    price_cost_effective_list = list()
    price_discount_list = list()

    environment_decoration_list = list()
    environment_noise_list = list()
    environment_space_list = list()
    environment_cleaness_list = list()

    dish_portion_list = list()
    dish_taste_list = list()
    dish_look_list = list()
    dish_recommendation_list = list()

    others_overall_experience_list = list()
    others_willing_to_consume_again_list = list()

    for i in range(len(read_csv_data["id"])):


            location_traffic_convenience_list.append(read_csv_data["location_traffic_convenience"][str(i)])
            location_distance_from_business_district_list.append(read_csv_data["location_distance_from_business_district"][str(i)])
            location_easy_to_find_list.append(read_csv_data["location_easy_to_find"][str(i)])

            service_wait_time_list.append(read_csv_data["service_wait_time"][str(i)])
            service_waiters_attitude_list.append(read_csv_data["service_waiters_attitude"][str(i)])
            service_parking_convenience_list.append(read_csv_data["service_parking_convenience"][str(i)])
            service_serving_speed_list.append(read_csv_data["service_serving_speed"][str(i)])

            price_level_list.append(read_csv_data["price_level"][str(i)])
            price_cost_effective_list.append(read_csv_data["price_cost_effective"][str(i)])
            price_discount_list.append(read_csv_data["price_discount"][str(i)])

            environment_decoration_list.append(read_csv_data["environment_decoration"][str(i)])
            environment_noise_list.append(read_csv_data["environment_noise"][str(i)])
            environment_space_list.append(read_csv_data["environment_space"][str(i)])
            environment_cleaness_list.append(read_csv_data["environment_cleaness"][str(i)])

            dish_portion_list.append(read_csv_data["dish_portion"][str(i)])
            dish_taste_list.append(read_csv_data["dish_taste"][str(i)])
            dish_look_list.append(read_csv_data["dish_look"][str(i)])
            dish_recommendation_list.append(read_csv_data["dish_recommendation"][str(i)])

            others_overall_experience_list.append(read_csv_data["others_overall_experience"][str(i)])
            others_willing_to_consume_again_list.append(read_csv_data["others_willing_to_consume_again"][str(i)])


    return location_traffic_convenience_list, location_distance_from_business_district_list, \
            location_easy_to_find_list, service_wait_time_list, \
            service_waiters_attitude_list, service_parking_convenience_list, \
            service_serving_speed_list, price_level_list, \
            price_cost_effective_list, price_discount_list, \
            environment_decoration_list, environment_noise_list, \
            environment_space_list, environment_cleaness_list, \
            dish_portion_list, dish_taste_list,\
            dish_look_list, dish_recommendation_list,\
            others_overall_experience_list, others_willing_to_consume_again_list 

def five_star_calculate(positve_number, negative_number, total_number):

    return round((positve_number - negative_number) / total_number, 1)

def five_star_condition(result):

    if result == -1:
        return "0"
    
    if result == 1:
        return "5"

    if result > -1 and result <= -0.6:
        return "1"

    if result > -0.6 and result <= -0.2:
        return "2"

    if result > -0.2 and result <= 0.2:
        return "3"

    if result > 0.2 and result <= 0.6:
        return "4"
    
    if result > 0.6 and result < 1:
        return "5"
    
def five_star_calculation(read_csv_data):

    each_comment_polarity_list = each_comment_polarity(read_csv_data)

    each_comment_five_star_list = list()
    
    for i, data in enumerate(each_comment_polarity_list):
        comment_counter = Counter(data)

        comment_total = comment_counter[1] + comment_counter[0] + comment_counter[-1]

        caculate_result = five_star_calculate(comment_counter[1], comment_counter[-1], comment_total)

        # call function
        each_comment_five_star_list.append({i : five_star_condition(caculate_result)})

    return each_comment_five_star_list
