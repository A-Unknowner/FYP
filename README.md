# KMU 2023 FYP - Keith - 4 (Aspect-Based Sentiment Analysis for Online Restaurant Review in Chinese)

## Environment
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
* Tensorflow-gpu need to download "[cuda toolkit](https://developer.nvidia.com/cuda-toolkit-archive) version `9.2` or `9.0`" and "[cudnn](https://developer.nvidia.com/rdp/cudnn-archive) for CUDA `9.2` or `9.0`" from NVIDIA official site

## Running the application
### 1. Download Model and Datasets
```bash
https://mailouhkedu-my.sharepoint.com/:u:/g/personal/s1302457_live_hkmu_edu_hk/EYoUn1tv61dEvaoAMfA8f8EBD673MpvmtttlERdFcKZBAw?e=60burc
```
- step1: Download the [final_cantonese_model.zip](https://mailouhkedu-my.sharepoint.com/:u:/g/personal/s1302457_live_hkmu_edu_hk/EYoUn1tv61dEvaoAMfA8f8EBD673MpvmtttlERdFcKZBAw?e=60burc) file
- step2: unzip the [final_cantonese_model.zip](https://mailouhkedu-my.sharepoint.com/:u:/g/personal/s1302457_live_hkmu_edu_hk/EYoUn1tv61dEvaoAMfA8f8EBD673MpvmtttlERdFcKZBAw?e=60burc) file
- step3: copy sub folder and sub file to `web/controller`. 
### 2. To run the application:
```bash
python ./web/index.py
```
## License
[MIT](https://github.com/A-Unknowner/FYP/blob/main/LICENSE)