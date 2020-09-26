'''
採用異步方式避免非阻塞，爬取bestofwine的威士忌資訊
'''
import requests ,time
import pandas as pd
from bs4 import BeautifulSoup
import os
import asyncio
import multiprocessing as mp
import aiohttp


headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

columns =['酒名','酒廠','url','年分','產地','酒精度(%)','照片','內容','評論','價錢']

def visit_MP ():
    permit =True
    c =0
    l =[]
    while permit:
        url = 'https://bestofwines.com/whisky/?type=7%2C10%2C15%2C16&view=grid&' \
              'price_min=%E2%82%AC%2010%2C-&price_max=%E2%82%AC%2040.000%2C-&offset={}&limit=60'.format(c)
        res = requests.get(url,headers=headers)
        soup = BeautifulSoup(res.text ,'html.parser')
        whisky_list = soup.select('a[class="tile-wrapper show-wine"] ')

        for whisky in whisky_list:
            url = 'https://bestofwines.com'+ whisky['href']
            print(url)
            l.append(url)

        c+=60
        if len(whisky_list) <60: permit=0
    return l
html_list=[]
async  def crawl(url,session):
    r = await session.get(url)
    html = await r.text()
    html_list.append([url,html])
    # return html

fine_list =[]
def get_info(list):
    c=1
    for url,html in list:
        soup = BeautifulSoup(html, 'html.parser')
        whisky_soup = soup.select('article[id="wine-detail"]')[0]
        #scatch value to variety
        whisky_name = whisky_soup.select('h1[itemprop="name"] span')[0].text
        distillery = whisky_soup.select('h1[itemprop="name"]')[0].text.split(whisky_name)[0]
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
        print('done:',c)
        c+=1

async def main():
    pool=mp.Pool(5)
    url_list = visit_MP()
    async with aiohttp.ClientSession() as session:
        print('crawling')
        tasks = [asyncio.create_task(crawl(url, session)) for url in url_list]
        await asyncio.wait(tasks)
        print(len(html_list))

        print('\nDistributed Parsing...')
        pool.apply_async(get_info(html_list))

        df = pd.DataFrame(columns=columns)
        df = df.append(pd.DataFrame(fine_list, columns=columns))

        # save
        if not os.path.exists('whisky_ETL'):
            os.mkdir('whisky_ETL')
        df.to_excel(r'./whisky_ETL/BOW3 .xlsx', index=None, encoding='utf-8', engine='xlsxwriter')

        print('done!')


if __name__ =='__main__':
    start =time.time()
    asyncio.run(main())
    print(time.time()-start)
