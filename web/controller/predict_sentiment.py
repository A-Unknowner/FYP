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
    if "openrice" in filename:
      original_test_data = os.path.join(dirname, filename)
      predict_save_file = os.path.join(dirname, predict_save_name)

  # if file is exist, remove it
  print("\n\n\npredict_save_file",predict_save_file,"\n\n\n")
  if os.path.isfile(predict_save_file):
    os.remove(predict_save_file)

  test_data = pd.read_csv(original_test_data)

  test_data.iloc[:, 1] = ""  # erase contents
  test_data.iloc[:, 2:] = predicts  # replace in place
  test_data.to_csv(predict_save_file, index=False)


def predict(unused):
  params = Params("params.yaml")

  test_path = "data/openrice"

  model_dir = "output"

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
  config = tf.estimator.RunConfig(
      model_dir=model_dir,
      tf_random_seed=params.random_seed,
      keep_checkpoint_max=params.keep_checkpoint_max,
      save_checkpoints_steps=params.save_n_step,
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
                         "openrice_restaurant_predict_result.csv")

def main():

  # Enable logging for tf.estimator
  tf.logging.set_verbosity(tf.logging.INFO)
  tf.app.run(predict)


if __name__ == "__main__":
  main()



