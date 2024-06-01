import pandas as pd
import numpy as np

import re
import unicodedata
from pyvi import ViTokenizer

import os

# Lấy đường dẫn tuyệt đối đến thư mục chứa preprocess_nhan.py
current_dir = os.path.dirname(os.path.abspath(__file__))
TEENCODE = os.path.join(current_dir, 'teencode.txt')

# TEENCODE = 'teencode.txt'
teencode_df = pd.read_csv(TEENCODE,names=['teencode','map'],sep='\t',)
teencode_list = teencode_df['teencode'].to_list()
map_list = teencode_df['map'].to_list()

stopwords_path = os.path.join(current_dir, 'vietnamese-stopwords-dash.txt')
# stopwords_path = 'vietnamese-stopwords-dash.txt'
with open(stopwords_path, "r", encoding='utf-8') as ins:
    stopword = []
    for line in ins:
        stopword.append(line.strip('\n'))

def searchTeencode(word):
  try:
    
    index = teencode_list.index(word)
    map_word = map_list[index]
    
    return map_word
  except:
    pass

def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
                               u"\U0001FA70-\U0001FAFF"  # chess symbols
                               u"\U00002600-\U000026FF"  # miscellaneous symbols
                               u"\U0001F18E-\U0001F1E6-\U0001F1FF"  # flags
                               "]+", flags=re.UNICODE)
    # emoji_pattern = regex.compile(r'\p{Emoji}', flags=regex.UNICODE)
    
    return emoji_pattern.sub(r'', string)

# remove_emoji("🥰🥰🥰 w 1")


def preprocess(text):
    # chuyển chữ thường
    text = str(text).lower()

    # chuẩn hóa unicode
    text = unicodedata.normalize('NFC', text)

    # xóa emoji
    text = remove_emoji(text)

    # loại bỏ kí tự đặc biệt
    # text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'[^\w\s]', ' ', text)

    #Teencode
    word_list = text.split()
    for tokens_idx, text_tokens in enumerate(word_list):
        deteencoded = searchTeencode(text_tokens)
        if (deteencoded != None):
            word_list[tokens_idx] = deteencoded

    text = (" ").join(word_list)

    # tách từ
    text = ViTokenizer.tokenize(text)
    

    # Loại bỏ stopword
    word_list = text.split()
    filtered_tokens = [word for word in word_list if word not in stopword]

    text = (" ").join(filtered_tokens)

    return text



