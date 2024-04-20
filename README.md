# KMU 2023 FYP - Keith - 4 (Aspect-Based Sentiment Analysis for Online Restaurant Review in Chinese)

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
pip install https://download.pytorch.org/whl/cu100/torch-1.0.1-cp36-cp36m-win_amd64.whl
```
* Tensorflow-gpu need to download "[cuda toolkit](https://developer.nvidia.com/cuda-toolkit-archive) version `9.2` or `9.0`" and "[cudnn](https://developer.nvidia.com/rdp/cudnn-archive) for CUDA `9.2` or `9.0`" from NVIDIA official site

## Running the application
### 1. Download Model and Datasets
```bash
https://mailouhkedu-my.sharepoint.com/:u:/g/personal/s1302457_live_hkmu_edu_hk/EYoUn1tv61dEvaoAMfA8f8EBD673MpvmtttlERdFcKZBAw?e=60burc
```
- step1: Download the [final_cantonese_model.zip](https://mailouhkedu-my.sharepoint.com/:u:/g/personal/s1302457_live_hkmu_edu_hk/EYoUn1tv61dEvaoAMfA8f8EBD673MpvmtttlERdFcKZBAw?e=60burc) file
- step2: unzip the [final_cantonese_model.zip](https://mailouhkedu-my.sharepoint.com/:u:/g/personal/s1302457_live_hkmu_edu_hk/EYoUn1tv61dEvaoAMfA8f8EBD673MpvmtttlERdFcKZBAw?e=60burc) file
- step3: copy the folders `chinese_vectors`, `data`, `output`, and `summary` to `web/controller`. 
### 2. To run the application:
```bash
python ./web/index.py
```
## License
[Apache](https://github.com/A-Unknowner/FYP/tree/main?tab=Apache-2.0-1-ov-file)
