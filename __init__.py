import imp
import os
import platform
import subprocess

if platform.system() == "Windows":
    os.chdir("./scrapy_openrice")
    print(os.popen("scrapy crawl openrice").read())
# try:
#     imp.find_module('scrapy')
#     found = True
# except ImportError:
#     found = False
# if found:
#     os.system("""pip install https://download.pytorch.org/whl/cu110/torch-1.7.0%2Bcu110-cp36-cp36m-win_amd64.whl;
#                  pip install spacy;
#                  pip install scikit-learn;
#                  pip install scrapy;
#                  mamba install m2-base""")
#     # os.popen("python -m pip install --upgrade pip").read()
#                      # pip install https://download.pytorch.org/whl/cu110/torch-1.7.0%2Bcu110-cp36-cp36m-win_amd64.whl;
#                      # pip install spacy;
#                      # pip install scikit-learn;
#                      # pip install scrapy;
#                      # mamba install m2-base""")
# else:
#     os.system("""python -m pip install --upgrade pip;
#                  pip install https://download.pytorch.org/whl/cu110/torch-1.7.0%2Bcu110-cp36-cp36m-win_amd64.whl;
#                  pip install spacy;
#                  pip install scikit-learn;
#                  pip install scrapy;
#                  mamba install m2-base""")
# os.chdir("./scrapy_openrice")
# print(os.popen("scrapy crawl openrice").read())