# -*- coding:utf-8 -*-
"""
1. 使用jieba进行分析，得到高频出现的词汇
2. 使用wordcloud制作词云
"""
import os
import sys
from jieba import analyse
from scipy.misc import imread
from wordcloud import WordCloud

reload(sys)
sys.setdefaultencoding('utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAX_WORDS = 500


def get_words(path):
    with open(path, 'r') as f:
        content = f.read()
    return analyse.textrank(content,topK=MAX_WORDS,withWeight=True)


def draw_wordcloud(words):
    img_path = os.path.join(BASE_DIR, 'zhanlang.png')
    font_path = os.path.join(BASE_DIR, 'simsun.ttc')
    back_coloring = imread(img_path)
    wordcloud = WordCloud(
        font_path=font_path,
        background_color="white",
        max_words=MAX_WORDS,
        mask=back_coloring,
        max_font_size=80,
        random_state=42
    ) 
    wordcloud.generate_from_frequencies(dict(words))
    wordcloud_img_path = os.path.join(BASE_DIR, 'zhanlang_word_cloud.png')
    wordcloud.to_file(wordcloud_img_path)


def main():
    text_path = os.path.join(BASE_DIR, 'zhanlang_comments')
    words = get_words(text_path)
    draw_wordcloud(words)
    

if __name__ == '__main__':
    main()

