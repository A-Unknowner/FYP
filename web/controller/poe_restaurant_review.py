from poe_api_wrapper import PoeApi

import json

bot = "gpt3_5"

# please paste your token here
TOKEN = ""

message = """
Please classify positive/neutral/negative sentiments on aspect checklist from the following restaurant review, 
also tag the word(noun) for target and reply the target sentence in Traditional Chinese, 
the output must contain the target and target sentence:

aspect checklist:
- Food prices
- Food quality
- Food style options
- Restaurant hygiene
- Restaurant service
- Restaurant general
- Restaurant prices
- Restaurant location
- Restaurant ambience

The output must same with the following template:
- Target Noun:
- Target Aspect:
- Sentiment:
- Original Target Sentence:

The following Traditional Chinese restaurant reviews is/are the input(s):
"""

def web_client():

    # test input
    input = """
    - 海鮮硬既有屎，牛肉發霉，碗碟非常非常非常唔乾淨。
    - 甜品是兩件毫無誠意的綠茶糕， 很難食 侍應人手不足，亦欠禮貌，希望管理層看到此投會有所改善
    - 路邊攤小食拼盤有南乳雞、澎湖花枝丸、台灣腸,全部都係台灣既美食。 炸地瓜條 真係好香脆,而且佢落左小小粉,又幾夾下。
    """
    
    # Using Client with proxy (default is False)
    client = PoeApi(TOKEN, proxy=True)

    outputs = str()

    try:
        response = client.send_message(bot, message + input)
        for chunk in response:
            outputs += chunk["response"]

        # the following commented code used to print out the results directly
        # for chunk in client.send_message(bot, message):
        #     print(chunk["response"], end="", flush=True)
        # print("\n")
    except RuntimeError:
        return "ChatGPT do not response"

    splited_output = outputs.split("\n")
    comments = list()
    review = dict()

    for output in splited_output:

        if output != "":
            data = output.split(":")
            result_key = data[0].replace("-", "").strip()
            result_value = data[1].replace("-", "").strip()

            match result_key:
                case "Target Noun": review["target_word"] = result_value

                case "Target Aspect": review["target_aspect"] = result_value

                case "Sentiment": review["sentiment"] = result_value

                case "Original Target Sentence": review["sentence"] = result_value
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

if __name__ == "__main__":

    results = web_client()

    print(results.decode())
    
