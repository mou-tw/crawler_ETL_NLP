import re
import pandas as pd
import numpy as np
import spacy
import en_core_web_lg
from unwanted_list import *
from make_array_func import make_array_func1 , make_array_func2

nlp = en_core_web_lg.load()
POS_lst =['PROPN', 'NOUN','VERB','ADV','ADJ']
count_dict = {}
to_array_lst =[]
whiskey_name_lst =[]

df = pd.read_csv('E:\DataCleaning\csv\Flavier.csv',encoding='ANSI')
#取出個別的威士忌名稱、內容和評論
for i in range(len(df)):
    try:
        whisky_name = df.iloc[i]['酒名']
        whisky_content = df.iloc[i]['內容']
        ret_content = re.sub('[\n\t\r?/.,]',' ',whisky_content)  #去除雜訊
        ret_content_lst = ret_content.split(' ')                #取得內容關鍵字列表
        ret_content_lst = [i for i in ret_content_lst if i.lower() not in list1] #取得乾淨列表
        '''
        # print(ret_content_lst)
        # for w in ret_content_lst:
        #     if w not in count_dict:
        #         count_dict[w] = 1
        #     else:
        #         count_dict[w] += 1
        
        '''
        ret = make_array_func1(ret_content_lst)
        # print(ret)

        whisky_comment = df.iloc[i]['評論']
        ret_comment = re.sub('[\n\t\r?/.,\[\]\';\(\)!:-]', ' ', whisky_comment)
        ret_comment_lst = ret_comment.split(' ')
        ret_comment_lst = [i for i in ret_comment_lst if i.lower() not in list1]
        '''
                print(ret_comment_lst)
        for w in ret_comment_lst:
            if w not in count_dict:
                count_dict[w] = 1
            else:
                count_dict[w] += 1
        '''
        ret2 = make_array_func2(ret,ret_comment_lst)
        print(ret2)
        to_array_lst.append(ret2)
        whiskey_name_lst.append(whisky_name)  #修改特正向量

    except:
        print('&&&&&&&&&&&&&&&&&&&'+whisky_name)
    print('>>>>>>>>>>>>')
# count_dict = sorted(count_dict.items() ,key= lambda x:x[1],reverse= True)
# print(count_dict)

print(whiskey_name_lst)
print(len(whiskey_name_lst))
print(to_array_lst)
whiskey_array = np.array(to_array_lst)
print(whiskey_array.shape)



