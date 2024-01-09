import poe
from poe_api_wrapper import PoeApi

import json

bot = "gpt3_5"

# please paste your token here
TOKEN = ["GPhGTPtn-7CsrpiZCYUdtw%3D%3D", "DAnCECIvdteAAK0dpD2Gvw%3D%3D"]

"""
ChatGPT Prompt Formula notes:
https://www.youtube.com/watch?v=jC4v5AS4RIM

Important
|       [task]
|       [context]
|       [exemplar]
|       [persona]
|       [format]
|       [tone]
Optional

"""

message = """
- You are the researcher of Aspect-Category Sentiment Analysis and you have to classify the given Cantonese restaurant review to the aspects of Food prices, Food quality, Food style options, Restaurant hygiene, Restaurant service, Restaurant general, Restaurant prices, Restaurant location, and Restaurant ambience, and classify these aspects with positive/neutral/negative sentiment, no need to output the result if the review no mentioned. Provide the outputs according to this structure:
Target Noun: [Original Cantonese text only]
Target Aspect: [Aspect]
Target Sentiment: [Sentiment]
Target Sentence: [Original Cantonese text only]

- Example1:
Target Noun: 火山排骨
Target Aspect: Food quality
Target Sentiment: Positive
Target Sentence: 火山排骨令到我念念不忘餐廳野食唔錯

- Example2:
Target Noun: 火山排骨
Target Aspect: Food prices
Target Sentiment: Positive
Target Sentence: 火山排骨既量多到嚇親我

- Example3:
Target Noun: 碗碟
Target Aspect: Restaurant hygiene
Target Sentiment: Positive
Target Sentence: 碗碟非常乾淨。

- This is the Cantonese restaurant review:
"""


def acsa_result(input = str()):
    # test input 1
    # input = "海鮮硬既有屎，牛肉發霉，碗碟非常非常非常唔乾淨。甜品是兩件毫無誠意的綠茶糕， 很難食 侍應人手不足，亦欠禮貌，希望管理層看到此投會有所改善。路邊攤小食拼盤有南乳雞、澎湖花枝丸、台灣腸,全部都係台灣既美食。 炸地瓜條 真係好香脆,而且佢落左小小粉,又幾夾下。"
    
    # test input 2
    #input = "/依間餐廳黎左第二次依到既火山排骨令到我念念不忘餐廳野食唔錯，坐位闊落岩晒一大班人黎食飯.火山排骨，$228上到黎依到既排骨既量多到嚇親我真係堆到好似火山咁既款，依到既排骨肉煮到好淋食落酸酸辣辣既味道，份量就大約3人既量.泰式燒魷魚依到既燒魷魚唔會燒到好老，食落去仲帶有少少脆口配上秘制醬酸酸辣好惹味.椰菜苗（蒜蓉炒）蒜蓉味十足啲菜炒到好有鑊氣.泰式滷水豬手依個豬手有好多醬汁，啲豬手炆到好淋肥瘦適中，好岩送飯"

    # test input 3
    input = "泰國菜真係每個月都必須食嘅 菜式今次又係去銅鑼灣食，不過又去另一間。\"`'-.,,.-'`\"-.,,.-`'`-.,,.-`'`-.,,.-*生蝦刺身（6隻) $108食泰國嘢必叫嘅生蝦！爽彈又大隻，配埋泰式醬汁真係好開胃生菜肉碎包有海量嘅肉碎 就 算一塊菜包好多肉碎都唔怕另外鍾意佢夠辣，不過真係堅辣怕辣之人唔好叫啊飛天椰菜苗 去泰國永遠都搵唔到嘅椰菜苗，喺香港食泰國嘢就必食！爽爽地嘅口感配口辣度，香口非常！泰式串燒 $108將外脆又厚肉嘅串燒沾滿沙嗲醬汁，非常juicy。黃咖喱雞肉 $108紅/黃/青咖喱當中，我始終都係最鍾意黃咖喱因為甜甜地、結結地，又唔會過份辣！配薄餅係最佳，索汁之餘亦冇白飯咁滯"
    
    input = input.replace('"',"")
    outputs = str()

    for cookie in TOKEN:
        try:
            # Using Client with proxy (default is False)
            client = PoeApi(cookie=cookie, proxy=True)
            chat_code = get_history_chat_bot(client=client)
            response = client.send_message(bot, message + input, chatCode=chat_code)
            for chunk in response:
                outputs += chunk["response"]

            break

            # the following commented code used to print out the results directly
            # for chunk in client.send_message(bot, message):
            #     print(chunk["response"], end="", flush=True)
            # print("\n")
        except RuntimeError:
            return f"{cookie} do not response"

    splited_output = outputs.split("\n")
    comments = list()
    review = dict()

    for output in splited_output:

        if output != "":
            data = output.split(":")
            result_key = data[0].replace("-", "").strip()
            result_value = data[1].replace("-", "").strip()

            match result_key:
                case "Target Noun":
                    review["target_word"] = result_value

                case "Target Aspect":
                    review["target_aspect"] = result_value

                case "Sentiment":
                    review["sentiment"] = result_value

                case "Original Target Sentence":
                    review["sentence"] = result_value
        else:
            comments.append(review)
            review = dict()

    # for testing
    # create a new chat
    history = client.get_chat_history(count=20)

    new_cursor = history['cursor']

    # create a new chat
    # Set a while loop with a condition of your choice
    while new_cursor != None:
        # Fetch the next 20 chat threads with new_cursor
        new_history = client.get_chat_history(count=20, cursor=new_cursor)
        # Append the next 20 chat threads 
        new_cursor = new_history['cursor']

    # return the result as json format
    return json.dumps(comments, ensure_ascii=False).encode('utf8')


def get_history_chat_bot(client: PoeApi):
    chat_bots = client.get_chat_history()['data']
    for chat_bot in chat_bots[bot]:
        if chat_bot['title'] == "Restaurant Sentiment Analysis":
            return chat_bot["chatCode"]
    return None


if __name__ == "__main__":
    results = acsa_result()

    print(results.decode())
