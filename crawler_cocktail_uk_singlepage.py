'''
單頁的爬蟲功能，提供函式供其他檔案使用
'''
import json
from bs4 import BeautifulSoup
import requests

class Cocktail:
    def __init__(self,name,recipe,url,content):
        self.name = name
        self.recipe = recipe
        self.url = url
        self.content =  content
        self.comment = []

# 清除除了英文和標點以外的字符
def clean_word(str):
    new_str = ''
    for s in str:
        if ord(s) <127: new_str +=s
    return new_str


def single_page_crawler(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

    res = requests.get(url, headers=headers)                        #取得響應訊息
    soup = BeautifulSoup(res.text, 'html.parser')                   #解析
    name = soup.select('h1[itemprop="name"]')[0].text
    name = clean_word(name)
    content = soup.select('p[itemprop="instructions"]')[0].text
    content = clean_word(content)
    recipe_list = soup.select('li[itemprop="ingredient"]')
    recipe_list = [clean_word(i.text.strip()).split('\n') for i in recipe_list] #將文字部分解析出並整理成新list
    # print(recipe_list)
    # print(name)
    # print(content)
    # print(recipe_list[0].text.strip())
    # sep = recipe_list[0].text.strip().split('\n')
    # print(sep)
    # for i in recipe_list:
    #     print(i.text.strip())

    cocktail_sample = Cocktail(name, recipe_list, url, content)     #實例化類型，並送入參數單
    print(cocktail_sample.__dict__)                                 #以字典方式將參數印出
    with open('./json_file/cocktail_test.json','a',encoding='utf-8') as f:
        f.write(json.dumps(cocktail_sample.__dict__)+'\n')


if __name__ == '__main__':
    url = 'https://www.cocktail.uk.com/cocktails/cosmopolitan'
    single_page_crawler(url)