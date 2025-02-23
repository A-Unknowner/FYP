# HKMU 2023 FYP - Keith - 4 (Aspect-Based Sentiment Analysis for Online Restaurant Review in Chinese)
## Application Name: Restaurant Review Analysis Tool for Cantonese
## Environment
Python 3.6.5

Environment installation cmd:
```bash
pip install opencc
pip install jieba --upgrade
pip install paddlepaddle-tiny==1.6.1
pip install jieba
pip install PyYAML==4.2b4
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
pip install prettytable
pip install scikit-learn
```
* Tensorflow-gpu need to download "[cuda toolkit](https://developer.nvidia.com/cuda-toolkit-archive) version `9.2` or `9.0`" and "[cudnn](https://developer.nvidia.com/rdp/cudnn-archive) for CUDA `9.2` or `9.0`" from NVIDIA official site

P.S: 

[FYP_2023_keith_4.zip](https://mailouhkedu-my.sharepoint.com/:u:/g/personal/s1303149_live_hkmu_edu_hk/EUT123lSM1dJv9P-jLzI50wBD1RZN_8Des_zTIrgpH2QvA?e=90ESEe)

There the file is `minconda3` or `anaconda3`' environment. Unzip it and copy sub file to folder `envs`. 
## Running the application
### 1. Download Model and Datasets
```bash
https://mailouhkedu-my.sharepoint.com/:u:/g/personal/s1302457_live_hkmu_edu_hk/EWHzAkiGrB9FiRkV6vo7ZQQByokoK8hmcxKF_65n4lXR1Q?e=kyiHKV
```
- step1: Download the [final_cantonese_model.zip](https://mailouhkedu-my.sharepoint.com/:u:/g/personal/s1302457_live_hkmu_edu_hk/EWHzAkiGrB9FiRkV6vo7ZQQByokoK8hmcxKF_65n4lXR1Q?e=kyiHKV) file
- step2: unzip the [final_cantonese_model.zip](https://mailouhkedu-my.sharepoint.com/:u:/g/personal/s1302457_live_hkmu_edu_hk/EWHzAkiGrB9FiRkV6vo7ZQQByokoK8hmcxKF_65n4lXR1Q?e=kyiHKV) file
- step3: copy the folders `chinese_vectors`, `data`, `output`, and `summary` to `web/controller`.

### 2. To run the application:
```bash
python ./web/index.py
```
### 3. To evaluate the model performance:
```bash
python ./web/evaluation_accuracy_f1.py
```
## License
[Apache](https://github.com/A-Unknowner/FYP/tree/main?tab=Apache-2.0-1-ov-file)
