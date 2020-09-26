import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

columns =['酒名','酒廠','url','年分','產地','酒精度(%)','照片','內容','評論','價錢']


def get_list():
    cataList =['scotch','world-whisky']
    l=[]
    for cata in cataList:
        url = 'https://flaviar.com/{}'.format(cata)
        res =requests.get(url,headers=headers)
        soup = BeautifulSoup(res.text ,'html.parser')
        whisky_list = soup.select('div[class="col-lg-3 col-md-4 col-sm-6"]')
        for spirit in whisky_list:
            url = 'https://flaviar.com/'+ spirit.select('a')[0]['href']
            pic_url = spirit.select('div[class="image flex flex--center flex--bottom-align lazy"] img ')[0]['data-src']
            l.append([url,pic_url])
    return l

def get_info(list):
    fine_list = []
    count=1
    for url,pic in list:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        detail_soup = soup.select('div[class="value"]')

        distillery = ''
        whisky_name = ''
        whisky_age = ''
        region = ''
        ABV = ''
        content = ''
        comment = []
        price = ''

        whisky_name = soup.select('div[class="product-info"] h1')[0].text
        region = detail_soup[0].text.strip()
        ABV = detail_soup[4].text.strip().replace('%', '')

        comment_list = soup.find_all('div', class_='txt')
        for c in comment_list:
            comment.append([c.text.strip().replace('\n', '')])
        try:
            distillery = detail_soup[5].text.strip()
            content = soup.select('div[class="p-content"] ')[0].text.strip()
            whisky_age = detail_soup[6].text.split('Year')[0].strip()
            price = soup.select('div[class="col-sm-7 price"] b')[0].text
        except IndexError:
            print(url)

        # put in list then return
        tmp_list =[whisky_name,distillery,url,whisky_age,region,ABV,pic,content,comment[3:],price]
        fine_list.append(tmp_list)
        print('done:',count)
        count+=1
    return fine_list





if __name__ =='__main__':
    whisky_list =get_list()
    detail_list = get_info(whisky_list)

    df = pd.DataFrame(columns=columns)
    df = df.append(pd.DataFrame(detail_list, columns=columns))

    # save
    if not os.path.exists('whisky_ETL'):
        os.mkdir('whisky_ETL')
    df.to_excel(r'./whisky_ETL/Flavier.xlsx', index=None, encoding='utf-8', engine='xlsxwriter')

    print('done!')