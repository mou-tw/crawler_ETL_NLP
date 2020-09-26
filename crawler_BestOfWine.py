import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

columns =['酒名','酒廠','url','年分','產地','酒精度(%)','照片','內容','評論','價錢']

def visit_MP ():
    '''
    set the default whisky url of the bestofwine main page
    request and set the info that I want
    then put all url in a list before return it
    :return:
    '''
    permit =True
    c =0
    l =[]
    while permit:
        url = 'https://bestofwines.com/whisky/?type=7%2C10%2C15%2C16&view=grid&' \
              'price_min=%E2%82%AC%2010%2C-&price_max=%E2%82%AC%2040.000%2C-&offset={}&limit=60'.format(c)
        res = requests.get(url,headers=headers)
        soup = BeautifulSoup(res.text ,'html.parser')
        whisky_list = soup.select('a[class="tile-wrapper show-wine"] ')

        print(len(whisky_list))
        for whisky in whisky_list:
            url = 'https://bestofwines.com'+ whisky['href']
            # print(name.text)
            print(url)
            # print('running')
            # with open('./pageurl.txt','a',encoding='utf-8')as f:
            #     f.write(url+'\n')
            l.append(url)
        c+=60
        if len(whisky_list) <60: permit=0
    return l

def get_info(list):
    fine_list =[]
    for url in list:
        res = requests.get(url,headers =headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        whisky_soup = soup.select('article[id="wine-detail"]')[0]
        #scatch value to variety
        distillery = whisky_soup.select('h1[itemprop="name"] span')[0].text
        whisky_name = whisky_soup.select('h1[itemprop="name"]')[0].text.split(distillery)[0]
        whiskyTable_soup = soup.select('div[id="wine-specs"] td')
        whisky_age = whiskyTable_soup[-15].text
        region = whiskyTable_soup[-17].text
        ABV = whiskyTable_soup[-9].text
        photo_url = 'https://bestofwines.com' + soup.select('a[class="enlarge-me"]')[0]['href']
        content = soup.select('div[id="wine-reviews"]')[0].text
        comment = None
        price = soup.select('span[class="price-big"]')[0].text.split('(')[0].strip()
        tmp_list = [whisky_name,distillery,url,whisky_age,region,ABV,photo_url,content,comment,price]
        fine_list.append(tmp_list)
        print('done')
    return fine_list



if __name__ =='__main__':
    url_list = visit_MP()
    detail_list = get_info(url_list)
    # print(len(url_list))
    df = pd.DataFrame(columns=columns)
    df = df.append(pd.DataFrame(detail_list, columns=columns))

    # save
    if not os.path.exists('whisky_ETL'):
        os.mkdir('whisky_ETL')
    df.to_excel(r'./whisky_ETL/BOW.xlsx',index=None, encoding='utf-8', engine='xlsxwriter')

    print('done!')