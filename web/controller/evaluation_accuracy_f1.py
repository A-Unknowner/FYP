import subprocess, os

# subprocess.run(["python", f"{os.getcwd()}/preprocess_data.py"])
import csv
import json
import os
import re

import jieba
import numpy as np
from prettytable import PrettyTable
from sklearn.metrics import accuracy_score, f1_score

from model.helper import Params

CHINESE_WORD_INT_PATH = f"{os.getcwd()}/chinese_vectors/word_idx_table.json"
STOPWORDS_PATH = f"{os.getcwd()}/chinese_vectors/cantonese_stopword.txt"


jieba.load_userdict('./cantonese_wordlist.txt')

def _add_sub_or_unk_word(word, vocab):
    res = []
    tmp = jieba.lcut(word, cut_all=True)
    for i in (0, -1):
        if tmp[i] in vocab:
            res.append(tmp[i])
    return res if len(res) > 0 else None


def _add_num_token(word):
    word = int(word)
    if word >= 10:
        return "<num>"  # 将数字 -> <num>
    else:
        return str(word)  # 0-9 保留


def tokenize_sentence(line, vocab):
    """句子分词

    Args:
        line (str): 原始的句子
        vocab (dict): 词/词组为key，index为value的字典

    Returns:
        list: 包含词/词组的index的列表
    """

    rule = re.compile("[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub('', line)

    sentence = []
    for word in jieba.cut(line, cut_all=False):
        if word in vocab:
            try:
                sentence.append(_add_num_token(word))
            except ValueError:
                sentence.append(word)
        else:
            sub_words = _add_sub_or_unk_word(word, vocab)
            if sub_words is not None:
                sentence += sub_words
    return sentence


def _write_rows_to_csv(lists, saved_csv_name):
    with open(saved_csv_name, 'w', newline='', encoding='utf-8', errors='ignore') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(lists)


def sentence_label_save(file_path, w2i_dict, params, test=False):
    """保存预处理完成的转型为int的sentence(sentence有长度截断)和one-hot后的labels (如果test=False)

    Args:
        file_path (str): 原始数据文件
        w2i_dict (dict): 语料库与int对应的字典
        params (Params object): 含有预处理所需参数的Params对象
        test (bool, optional): Defaults to False. 该文件是否为test, 若True则不输出labels

    """

    def _string_to_int_sentence(line, lookup_table, params):
        int_sentence = []
        num_idx = params.chinese_word_size
        # 经初步处理后sentence 超过的max_len的部分去除
        if len(line) > params.max_len:
            line = line[:params.max_len]
        for word in line:
            if word == "<num>":
                int_sentence.append(num_idx)
            else:
                int_sentence.append(lookup_table[word])
        return int_sentence

    def _one_hot_label(label, one_hot_len):
        label_one_hot = np.array([0] * 80)
        idx = [x + 2 + 4 * i for i, x in enumerate(label)]
        label_one_hot[idx] = 1
        return list(label_one_hot)

    labels = []
    sentences_idx_path = os.path.join(
        f"{os.getcwd()}/data/val"
        # os.path.dirname(file_path)
        , "sentences_idx.csv")

    with open(sentences_idx_path, 'w', newline='') as save_idx_f:
        writer_idx = csv.writer(save_idx_f, delimiter=',')
        with open(file_path, newline='', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader)
            for idx, sentence, *label in reader:
                sentence = tokenize_sentence(sentence, w2i_dict)
                sentence_idx = _string_to_int_sentence(
                    sentence, w2i_dict, params)
                if not test:
                    label = [int(x) for x in label]
                    # one-hot for each label category
                    label = _one_hot_label(label, one_hot_len=80)
                    labels.append(label)
                writer_idx.writerow(sentence_idx)

    labels_path = os.path.join(os.path.dirname(file_path), "labels.csv")
    if not test:
        _write_rows_to_csv(labels, labels_path)


def load_chinese_table(chinese_path, stopwords_path):
    """返回去除停止词的word转int的词典

    Args:
        chinese_path (str): 中文词向量json文件地址
        stopwords_path (str): 中文停用词地址

    Returns:
        dict: 返回 word->int 对应的字典
    """

    with open(chinese_path, encoding='utf-8') as f:
        word_int_table = json.load(f)

    stopwords = set()
    with open(stopwords_path, 'r', encoding='gb2312', errors='ignore') as f:
        for stopword in f:
            stopwords.add(stopword.strip())

    return {k: v for k, v in word_int_table.items() if k not in stopwords}


def main1():
    params = Params(f"{os.getcwd()}/params.yaml")
    word_int_table = load_chinese_table(CHINESE_WORD_INT_PATH, STOPWORDS_PATH)
    dataset_path = f"{os.getcwd()}/data/val/val_sc.csv"

    # dataset_path = os.path.join(
    #     data_dir, os.path.basename(data_dir) + "_sc.csv")
    sentence_label_save(
        dataset_path, word_int_table, params)

# subprocess.run(["python", f"{os.getcwd()}/predict_sentiment.py"])
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from model.helper import Params
from model.input_fn import build_dataset, input_fn
from model.model_fn import model_fn


# prediction result
def save_or_update_predict(predicts,
                           dirname,
                           predict_save_name):
    """将推断得到的predicts按要求格式保存到本地

    Args:
        predicts (numpy array): 模型预测得到的结果集合
        dirname (str): 测试集所在的文件夹地址
        predict_save_name (str): 保存到本地的文件名称
    """
    print("\n\n\nrunning\n\n\n")

    for filename in os.listdir(dirname):
        if "val" in filename:
            original_test_data = os.path.join(dirname, filename)
            predict_save_file = os.path.join(dirname, predict_save_name)

    # if file is exist, remove it
    print("\n\n\npredict_save_file", predict_save_file, "\n\n\n")
    if os.path.isfile(predict_save_file):
        os.remove(predict_save_file)

    test_data = pd.read_csv(original_test_data)

    test_data.iloc[:, 1] = ""  # erase contents
    test_data.iloc[:, 2:] = predicts  # replace in place
    test_data.to_csv(predict_save_file, index=False)


def predict(unused):
    params = Params(f"{os.getcwd()}/params.yaml")

    test_path = f"{os.getcwd()}/data/val"

    model_dir = f"{os.getcwd()}/output"

    # load test data
    test_feature = build_dataset(
        os.path.join(test_path, "sentences_idx.csv"),
        length=params.max_len,
        padding=True)
    test_label = build_dataset(  # pseudo labels
        None,
        length=params.multi_categories * params.num_sentiment,
        padding=False,
        cascading_label=True,
        label_num=params.num_sentiment)

    def test_input_fn():
        return input_fn(test_feature,
                        test_label,
                        batch_size=1,
                        is_training=False,
                        is_test=True,
                        repeat_count=1)

    # define config
    session_config = tf.ConfigProto()
    session_config.gpu_options.per_process_gpu_memory_fraction = 1
    session_config.gpu_options.allow_growth = True

    # define config
    config = tf.estimator.RunConfig(
        model_dir=model_dir,
        tf_random_seed=params.random_seed,
        keep_checkpoint_max=params.keep_checkpoint_max,
        save_checkpoints_steps=params.save_n_step,
        session_config=session_config
    )

    # define estimator
    nn = tf.estimator.Estimator(
        model_fn=model_fn,
        config=config,
        params=params
    )

    print("\n--Predict data--\n")

    predict_results = nn.predict(input_fn=test_input_fn)

    results = []
    for result in predict_results:  # result is dict object

        results.append(result["classes"])

    results = np.asarray(results)

    save_or_update_predict(results,
                           test_path,
                           "predict_data.csv")


def main2():
    # Enable logging for tf.estimator
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(predict)


def openrice_restaurant_predict_result(fiters, predictions_path):

    print("path ",os.path.exists(predictions_path))
    try:
        prediction = pd.read_csv(predictions_path)

        # return False, prediction
        return (len(prediction[fiters[0]])<=0, prediction)
    except FileNotFoundError:
        return (True, None)

if __name__ == "__main__":
    fiters = ["location_traffic_convenience", "location_distance_from_business_district", "location_easy_to_find",
              "service_wait_time", "service_waiters_attitude", "service_parking_convenience", "service_serving_speed",
              "price_level", "price_cost_effective", "price_discount", "environment_decoration", "environment_noise",
              "environment_space", "environment_cleaness", "dish_portion", "dish_taste", "dish_look",
              "dish_recommendation", "others_overall_experience", "others_willing_to_consume_again"]
    predict_data, pred = openrice_restaurant_predict_result(fiters, f"{os.getcwd()}/data/val/predict_data.csv")

    print(predict_data)
    if predict_data:
        main1()
        main2()
    true = pd.read_csv(f"{os.getcwd()}/data/val/val_sc.csv")
    true_array = np.array([true[fiter] for fiter in fiters])
    pred_array = np.array([pred[fiter] for fiter in fiters])
    print(f"all predictions: {len(true['content'])}")
    # Accuracy
    table = PrettyTable(["", "correct prediction", "accuracy"])
    for fiter in fiters:
        table.add_row([fiter, len([i for i, j in zip(true[fiter], pred[fiter]) if i == j]),
                       accuracy_score(true[fiter], pred[fiter])])
    print(table)
    print(f"accuracy:{sum([accuracy_score(true[fiter], pred[fiter]) for fiter in fiters]) / len(fiters)}")

    # F1
    table = PrettyTable(["", "correct prediction", "F1"])
    for fiter in fiters:
        table.add_row([fiter, len([i for i, j in zip(true[fiter], pred[fiter]) if i == j]),
                       f1_score(true[fiter], pred[fiter], average='macro')])
    print(table)
    print(f"F1:{sum([f1_score(true[fiter], pred[fiter], average='macro') for fiter in fiters]) / len(fiters)}")
