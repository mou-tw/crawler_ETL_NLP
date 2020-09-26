'''
先爬取全部的分頁資訊，並儲存為文字檔，最後引入單頁爬蟲函式
'''

from bs4 import BeautifulSoup
import requests
from crawler_cocktail_uk_singlepage import single_page_crawler


def get_all_url():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    for i in range(1, 3):
        url = 'https://www.cocktail.uk.com/cocktails?page={}'.format(i)
        print(url)
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        url_list = soup.select('div[class="column small-11"] a')  # 取得分頁列表
        for url in url_list:
            r_url = 'https://www.cocktail.uk.com' + url['href']
            with open('cock_url.txt', 'a+', encoding='utf-8')as f:
                if r_url not in f.read():
                    f.write(r_url + '\n')
            print(r_url)


def get_pageinfo():
    with open('cock_url.txt', 'r', encoding='utf-8') as f:
        for url in f:
            single_page_crawler(url.strip())




if __name__ == '__main__':
    # main()
    get_pageinfo()
