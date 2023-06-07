#! /bin/env python
import requests
from collections import namedtuple
import os
import sys
import urllib.request
from bs4 import BeautifulSoup
import json

# this code is just for : [ http://dict.cn ]
FILE_PATH = '/home/zh/.myword'


def _connect(host='https://www.baidu.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False


def curlWordInfo(word):
    Word = namedtuple('Word', ["content", "definition", "pron"])
    URL = "http://dict.cn/{}"
    word_url = URL.format(word)
    req_content = requests.get(word_url).content.decode("utf-8")
    soup = BeautifulSoup(req_content, 'lxml')
    title = soup.title
    word_divs = soup.find_all('h1', class_="keyword")
    phonetic_divs = soup.find_all('bdo', lang="EN-US")
    trans_divs = soup.find_all('strong')

    # --------------------------------------------------------------------
    # bad check and assertion to prevent the currect result :)
    if (title.string == "该词条未找到_海词词典"):
        print(f"Not foud this word {sys.argv[-1]}")
        exit(0)
    assert (word_divs[0].string == word)
    assert (len(phonetic_divs) == 2)
    assert (len(trans_divs) >= 1)
    keyword = word
    # just use one item ; if you want to gain more info you can change my code
    phonetic = phonetic_divs[0].string[1:-1]
    temp = [trans_divs[i].string for i in range(len(trans_divs))]
    trans = " ".join(temp)
    return Word(keyword, trans, phonetic)


def word2json(word_info):
    word_dict = dict(word_info._asdict())
    word_json = json.dumps(word_dict, ensure_ascii=False)
    return word_json


def saveToFile(file_path, word):
    assert (os.path.exists(file_path) == True)
    with open(file_path, 'a+') as appender:
        appender.writelines(word)


def fmtOutput(wordobj):
    print(wordobj.content)
    print(wordobj.definition)
    print(wordobj.pron)


if __name__ == '__main__':
    assert (len(sys.argv) == 2)
    assert (_connect() == True)
    Word = namedtuple('Word', ["content", "definition", "pron"])
    word = curlWordInfo(sys.argv[-1])
    word_json = word2json(word)
    fmtOutput(word)
    saveToFile(FILE_PATH, word_json)

# ----------------------------------
#  class Word:
#
#      def __init__(self, keyword, phonetic, translate):
#          self.__keyword = keyword
#          self.__phonetic = phonetic
#          self.__translate = translate
#
#      @property
#      def keyword(self):
#          return self.__keyword
#
#      @property
#      def phonetic(self):
#          return self.__phonetic
#
#      @property
#      def translate(self):
#          return self.__translate
#
