from wordcloud import WordCloud
import numpy as np
import pandas as pd
import codecs
import jieba
jieba.load_userdict('../data/user_dict.txt')
from scipy.misc import imread
import os
from os import path
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import collections
from io import StringIO

KEYWORD = '口袋妖怪'
FILE_DIR = '../output/' + KEYWORD + '.txt'
SEP = 'XYX'

FONT = '../data/font.ttf'
MASK = '../data/pikachu.jpg'
IMG_DIR = '../output/wordcloud.jpg'

def get_word(text, isfile=False):
    with open('../data/stopwords.txt', 'r', encoding='utf-8') as f:
                stopwords = [line.strip() for line in f]
    if isfile:
        comment_text = open(text, 'r', encoding='UTF-8').read()
    else:
        comment_text = text
    
    return [word for word in jieba.cut(comment_text) if word not in stopwords]
    
def get_wordcloud(text, font_dir, mask_dir, img_dir, isfile=True, max_num=200, font_size=150):
    with open('../data/stopwords.txt', 'r', encoding='utf-8') as f:
                stopwords = [line.strip() for line in f]
    if isfile:
        comment_text = open(text, 'r', encoding='UTF-8').read()
    else:
        comment_text = text
    cut_text = " ".join([word for word in jieba.cut(comment_text) if word not in stopwords])
    
    color_mask = imread(mask_dir)
    cloud = WordCloud(
        font_path=font_dir,
        background_color='black',
        mask=color_mask,
        max_words=max_num,
        max_font_size=font_size,
        width=1280,height=720,
        #colormap='rainbow'
        colormap='Blues'
    )
    word_cloud = cloud.generate(cut_text)
    word_cloud.to_file(img_dir)
    
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()

def main(file_dir):
    comment_text = open(file_dir, encoding='UTF-8').read()
    data = StringIO(comment_text)
    df = pd.read_csv(data, sep=SEP)
    reply = [str(x) for x in df.reply]
    content = ' '.join(reply)

    font = FONT
    mask = MASK
    img_dir = IMG_DIR
    get_wordcloud(content, font, mask, img_dir, 0)

if __name__ == '__main__':
    file_dir = FILE_DIR
    main(file_dir)