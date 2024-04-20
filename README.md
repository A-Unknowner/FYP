# Environment
Python 3.6.5

Environment installation cmd:
```bash
pip install opencc
pip install jieba --upgrade
pip install jieba
pip uninstall numpy
pip uninstall pandas
pip install numpy==1.14.5
pip install pandas==0.23.4
pip install tensorflow-gpu==1.10.0
pip install flask
pip install lxml
pip install beautifulsoup4
pip install requests
pip install langdetect
```


download "cuda toolkit version 9.2" and "cudnn 9.2" from NVIDIA official site or "cuda toolkit version 9.0" and "cudnn 9.0" from NVIDIA official site

To run the code, please use the following cmd:

cd fsauor-master/Multi-task/Transformer+Convolutional
create folder call "data"
create 4 folders (call "a", "b", "train", "val") inside the "data" folder
download opencc-1.0.4-win32.7z and unzip it
add the opencc bin path to system variable
download the sgns.weibo.bigram-char.bz2 file and place it into "fsauor-master/Multi-task/Transformer+Convolutional/chinese_vectors" directory
cd fsauor-master/Multi-task/Transformer+Convolutional/chinese_vectors
python build_word_vectors.py
put the chinese_stopwords.txt into "fsauor-master/Multi-task/Transformer+Convolutional/chinese_vectors" directory 

bash ./train.sh

# Model and Datasets Download Link
```bash
https://mailouhkedu-my.sharepoint.com/:u:/g/personal/s1302457_live_hkmu_edu_hk/EYoUn1tv61dEvaoAMfA8f8EBD673MpvmtttlERdFcKZBAw?e=60burc

```


# model and data
```commandline
https://gitlab.com/hkmu/FYP.git
```
