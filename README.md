#Environment
Python 3.6
Environment installation cmd:
```commandline
python -m pip install --upgrade pip
pip install https://download.pytorch.org/whl/cu110/torch-1.7.0%2Bcu110-cp36-cp36m-win_amd64.whl
pip install spacy
pip install scikit-learn
pip install scrapy
mamba install m2-base
```


Please download this dataset:
[https://nlp.stanford.edu/data/glove.42B.300d.zip](https://nlp.stanford.edu/data/glove.42B.300d.zip)

To run the code, please use the following cmd:
bash ./train.sh

#comment
```commandline
cd ./scrapy_openrice
scrapy crawl openrice
scrapy crawl openrice -o [filename].csv
```
