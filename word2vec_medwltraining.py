'''
分別讀取先前爬取的網站評論，清理文字，並將分別評論以空格分隔，送進list中，形成list of list，給word2vec訓練用
'''
import numpy as np
import re
import pickle
import pandas as pd
from gensim.models import word2vec

tmp_lst = []

with open('./pickle_file/whisky_comment.pickle', 'rb') as f:
    tmp_lst=pickle.load(f)

print(len(tmp_lst))


model = word2vec.Word2Vec(tmp_lst,size=20,iter=3,window=2,min_count=15,workers=4)
model.save("./word2vec_model/word2vec_whisky.model")

print(model.wv.__getitem__('vanilla'))

print(model.wv.most_similar('sherry',topn=5))
print(model.wv.most_similar('vanilla',topn=6))