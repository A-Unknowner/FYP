# coding=utf-8
import os

from poe_api_wrapper import PoeApi
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
from prettytable import PrettyTable

bot = "gpt3_5"

# test_file = "./data/val/val_sc.csv"
# test_file = "./data/openrice/openrice_sc.csv"
# predict_file = "./data/openrice/chat_result.csv"
test_file = "./data/openrice/openrice_review.csv"
predict_file = "./data/openrice/chat_openrice_result.csv"

# please paste your token here
TOKEN = [
         "HcSV0SncdXrF1vl4XXvukg%3D%3D",
         "WDCVpn1PYrTnxdMCwrzVzg%3D%3D",
         "GPhGTPtn-7CsrpiZCYUdtw%3D%3D",
         "DAnCECIvdteAAK0dpD2Gvw%3D%3D",
         # "8kIDzmhtVqfh_2BfhxS5tA%3D%3D"
]

# message = """
# 現在進行廣東話的情緒分析，分析留言內的每個類別的情緒。["餐廳的交通是否便利", "餐廳的位置距離商圈遠近", "餐廳的位置是否容易尋找", "餐廳的服務排隊等候時間", "餐廳的服務人員態度", "餐廳的是否容易停車", "餐廳的點菜或上菜或送餐速度", "餐廳的價格水平", "餐廳的性價比", "餐廳的折扣力度", "餐廳的環境裝修狀況", "餐廳的吵雜狀況", "餐廳的用餐空間", "餐廳的環境衛生狀況", "餐廳的菜餚分量", "餐廳的菜餚味道", "餐廳的菜餚外觀", "餐廳的菜餚推薦程度", "本次消費感受", "再次消費的意願"]為留言的分析類別，而["正面", "正常", "負面", "沒有提及"]為每項類別的情緒分析。每個留言分析結果都有所有類別，並每個類別都有一個情緒分析。
# 請分析以下的留言並輸出所有類別的分析結果：
# """
message = """
你是一位資料科學家，你的任務是為廣東話評論進行情緒分析，分析其類別的情緒。下列["餐廳的交通是否便利", "餐廳的位置距離商圈遠近", "餐廳的位置是否容易尋找", "餐廳的服務排隊等候時間", "餐廳的服務人員態度", "餐廳的是否容易停車", "餐廳的點菜或上菜或送餐速度", "餐廳的價格水平", "餐廳的性價比", "餐廳的折扣力度", "餐廳的環境裝修狀況", "餐廳的吵雜狀況", "餐廳的用餐空間", "餐廳的環境衛生狀況", "餐廳的菜餚分量", "餐廳的菜餚味道", "餐廳的菜餚外觀", "餐廳的菜餚推薦程度", "本次消費感受", "再次消費的意願"]為評論的分析類別，而["評論正面 1", "評論正常 0", "評論負面 -1", "評論沒有提及 -2"]為每項類別的情緒。每個評論分析結果都有所有類別，並每個類別都有一個情緒。 請分析以下的評論並輸出所有類別的分析結果：
"""


# def analysis_result(input = str(), comments = list()):
def acsa_result(input):
    if os.path.isfile(predict_file):
        print(f"{predict_file} find!")
        result_csv = pd.read_csv(predict_file)
    else:
        print(f"{predict_file} not find!")
        result_csv = pd.DataFrame(columns=input.columns)

    for index, row in input.iterrows():
        if (os.path.isfile(predict_file) and index >= len(result_csv)) or (not os.path.isfile(predict_file)):
            result_csv = pd.concat([result_csv, row.to_frame().T], ignore_index=True)
            for cookie in TOKEN:
                try:
                    # Using Client with proxy (default is False)
                    client = PoeApi(cookie=cookie)
                    chat_code, isHistory = get_history_chat_bot(client=client)
                    while True:
                        outputs = str()
                        try:
                            response = client.send_message(bot, message + row["content"].replace('"', '').replace("\n", ""), chatCode=chat_code)
                            for chunk in response:
                                outputs += chunk["response"]
                        except Exception as e:
                            if "Daily limit reached for gpt3_5." in str(e):
                                raise RuntimeError("Daily limit reached")
                            client.cancel_message(chunk)
                            result_csv.loc[index, "content"] = e
                            print(row, e)
                            # print(row['content'].replace('"', '').replace("\n", ""))
                            if not isHistory:
                                chat_code, isHistory = get_history_chat_bot(client=client)
                            previous_messages = client.get_previous_messages(bot=bot, chatCode=chat_code, count=2)
                            right_row = False
                            for previous_message in previous_messages:
                                print(previous_message)
                                if previous_message["text"] == message + row["content"].replace('"', '').replace("\n", ""):
                                    result_csv.loc[index, "content"] = '"' + previous_message["text"].replace(message, '') + '"'
                                    right_row = True
                                if right_row:
                                    outputs = previous_message["text"]
                                    print(outputs)
                            if not right_row:
                                continue
                        splited_output = outputs.split(":")
                        print(splited_output)
                        print(len(splited_output))
                        if len(splited_output) > 20:
                            aspect_category(splited_output, result_csv, index)
                            if not isHistory:
                                chat_code, isHistory = get_history_chat_bot(client=client)
                        else:
                            chat_code = client
                            isHistory = False
                            continue
                        result_csv.to_csv(predict_file, encoding="utf_8_sig", index=False)
                        break
                    break
                except RuntimeError as e:
                    print(e)
                    print(f"{cookie} do not response")
                    TOKEN.remove(cookie)
def aspect_category(splited_output, result_csv, index):
    for i in range(len(splited_output)):
        # try:
        if "餐廳的交通是否便利" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "location_traffic_convenience"] = output
        elif "餐廳的位置距離商圈遠近" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "location_distance_from_business_district"] = output
        elif "餐廳的位置是否容易尋找" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "location_easy_to_find"] = output
        elif "餐廳的服務排隊等候時間" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "service_wait_time"] = output
        elif "餐廳的服務人員態度" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "service_waiters_attitude"] = output
        elif "餐廳的是否容易停車" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "service_parking_convenience"] = output
        elif "餐廳的點菜或上菜或送餐速度" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "service_serving_speed"] = output
        elif "餐廳的價格水平" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "price_level"] = output
        elif "餐廳的性價比" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "price_cost_effective"] = output
        elif "餐廳的折扣力度" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "price_discount"] = output
        elif "餐廳的環境裝修狀況" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "environment_decoration"] = output
        elif "餐廳的吵雜狀況" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "environment_noise"] = output
        elif "餐廳的用餐空間" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "environment_space"] = output
        elif "餐廳的環境衛生狀況" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "environment_cleaness"] = output
        elif "餐廳的菜餚分量" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "dish_portion"] = output
        elif "餐廳的菜餚味道" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "dish_taste"] = output
        elif "餐廳的菜餚外觀" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "dish_look"] = output
        elif "餐廳的菜餚推薦程度" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "dish_recommendation"] = output
        elif "本次消費感受" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "others_overall_experience"] = output
        elif "再次消費的意願" in splited_output[i]:
            output = sentiment(splited_output[i + 1])
            if output is not None:
                result_csv.loc[index, "others_willing_to_consume_again"] = output
    # except Exception as e:
    #     print(splited_output)
    #     print(splited_output[i])
    #     print(e)

# def sentiment(analysis_result):
#     if "正面" in analysis_result:
#         return 1
#     if "正常" in analysis_result:
#         return 0
#     if "負面" in analysis_result:
#         return -1
#     if "沒有提及" in analysis_result:
#         return -2
#     return 0
def sentiment(analysis_result):
    if "評論正面" in analysis_result:
        return 1
    if "評論正常" in analysis_result:
        return 0
    if "評論負面" in analysis_result:
        return -1
    if "評論沒有提及" in analysis_result:
        return -2
    return 0

def get_history_chat_bot(client: PoeApi):
    chat_bots = client.get_chat_history()['data']
    i = 0
    for chat_bot in chat_bots[bot]:
        if (chat_bot['title'] == "情緒分析" or chat_bot['title'] == "新的聊天") and i == 0:
            return chat_bot["chatCode"], True
        else:
            break
        i += 1
    return client, False

def get_accuracy_f1(test_csv, predict_csv):
    print(f"all predictions: {len(test_csv['content'])}")
    # Accuracy
    table = PrettyTable(["", "correct prediction", "accuracy"])
    for fiter in fiters:
        table.add_row([fiter, len([i for i, j in zip(test_csv[fiter], predict_csv[fiter]) if i == j]),
                       accuracy_score(test_csv[fiter], predict_csv[fiter])])
    print(table)
    print(f"accuracy:{sum([accuracy_score(test_csv[fiter], predict_csv[fiter]) for fiter in fiters]) / len(fiters)}")

    # F1
    table = PrettyTable(["", "correct prediction", "F1"])
    for fiter in fiters:
        table.add_row([fiter, len([i for i, j in zip(test_csv[fiter], predict_csv[fiter]) if i == j]),
                       f1_score(test_csv[fiter], predict_csv[fiter], average='macro')])
    print(table)
    print(
        f"F1:{sum([f1_score(test_csv[fiter], predict_csv[fiter], average='macro') for fiter in fiters]) / len(fiters)}")

if __name__ == "__main__":
    fiters = ["location_traffic_convenience", "location_distance_from_business_district", "location_easy_to_find",
              "service_wait_time", "service_waiters_attitude", "service_parking_convenience", "service_serving_speed",
              "price_level", "price_cost_effective", "price_discount", "environment_decoration", "environment_noise",
              "environment_space", "environment_cleaness", "dish_portion", "dish_taste", "dish_look",
              "dish_recommendation", "others_overall_experience", "others_willing_to_consume_again"]
    # test_file = "./data/val/val_sc.csv"
    if os.path.isfile(test_file):
        test_csv = pd.read_csv(test_file)
    else:
        print(f"{test_file} not find!")
        exit(0)

    acsa_result(test_csv)

    predict_csv = pd.read_csv(predict_file)

    if len(predict_csv) == len(test_csv):
        get_accuracy_f1(test_csv, predict_csv)
    else:
        print(f"complete predict {len(predict_csv)}/{len(test_csv)} {len(predict_csv)/len(test_csv)*100}%")

