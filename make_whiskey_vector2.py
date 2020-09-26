import re ,time
import pandas as pd
import numpy as np
import spacy
import en_core_web_lg
from unwanted_list import *
from make_array_func import make_array_func1 , make_array_func2

nlp = en_core_web_lg.load()
POS_lst =['PROPN', 'NOUN','VERB','ADV','ADJ']
unwanted_lst = ['appearance','color','flavor','smell','taste','palate','-']
save_lst = []
st = time.time()

def mk_vec_lit (lst):
    vec_lst = [0] * 16
    for w in lst:
        w = nlp(w)
        if (w.vector_norm):
            if w.similarity(nlp('sweet')) > 0.65:
                vec_lst[0] += 1
            if w.similarity(nlp('vanilla')) > 0.65:
                vec_lst[1] += 1
            if w.similarity(nlp('smoke')) > 0.5:
                vec_lst[2] += 1
            if w.similarity(nlp('roast')) > 0.5:
                vec_lst[3] += 1
            if w.similarity(nlp('wine')) > 0.5:
                vec_lst[4] += 1
            if w.similarity(nlp('grain')) > 0.5:
                vec_lst[5] += 1
            if w.similarity(nlp('fruit')) > 0.5:
                vec_lst[6] += 1
            if w.similarity(nlp('spice')) > 0.55:
                vec_lst[7] += 1
            if w.similarity(nlp('grass')) > 0.5:
                vec_lst[8] += 1
            if w.similarity(nlp('wood')) > 0.5:
                vec_lst[9] += 1
            if w.similarity(nlp('flower')) > 0.5:
                vec_lst[10] += 1
            if w.similarity(nlp('smooth')) > 0.5:
                vec_lst[11] += 1
            if w.similarity(nlp('heavy')) > 0.5:
                vec_lst[12] += 1
            if w.similarity(nlp('balance')) > 0.5:
                vec_lst[13] += 1
            if w.similarity(nlp('salt')) > 0.5:
                vec_lst[14] += 1
    return vec_lst


df = pd.read_csv('E:\DataCleaning\csv\Flavier.csv',encoding='ANSI')
for i in range(len(df)):
    try:
        tmp_lst =[]
        whisky_name = df.iloc[i]['酒名']
        whisky_content = df.iloc[i]['內容']
        ret = nlp(whisky_content)
        for word in ret:
            if word.pos_ in POS_lst and word.lemma_.lower() not in unwanted_lst:
                tmp_lst.append(word.lemma_.lower())
        whisky_comment = df.iloc[i]['評論']
        ret = nlp(whisky_comment)
        for word in ret:
            if word.pos_ in POS_lst and word.lemma_.lower() not in unwanted_lst:
                tmp_lst.append(word.lemma_.lower())

        print(tmp_lst)
        ret_lst = mk_vec_lit(tmp_lst)
        print(ret_lst)
        save_lst.append(ret_lst)

    except:
        print('&&&&&&&&&&&&&&&&&&&'+whisky_name)

with open('train2.csv','w',encoding='utf-8') as f:
    f.write(str(save_lst))


print(time.time()-st)