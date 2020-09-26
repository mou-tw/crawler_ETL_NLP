'''
爬取ptt，帶入cookie，取得文章內容後儲存成文字檔
'''
import requests , os
from bs4 import BeautifulSoup

resource_path = r'./res_gossiping'
if not os.path.exists(resource_path):
    os.mkdir(resource_path)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
ss = requests.session()
ss.cookies['over18'] = '1'

url = 'https://www.ptt.cc/bbs/Gossiping/index.html'

n = 30
for i in range(0,n):
    res = ss.get(url, headers = headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    article_title_html = soup.select('div[class="title"]')

    for each_article in article_title_html:
        try:
            print(each_article.a.text)
            print('https://www.ptt.cc' + each_article.a['href'])

            article_url = 'https://www.ptt.cc' + each_article.a['href']
            article_text = each_article.a.text
            article_text = article_text.replace('?','')

            article_res = ss.get(article_url, headers=headers)
            article_soup = BeautifulSoup(article_res.text, 'html.parser')

            push_up = 0
            push_down = 0
            score = 0
            author = ''
            title = ''
            datetime = ''
            try:
                article_content = article_soup.select('div#main-content')[0].text.split('--')[0]
                push_info_list = article_soup.select('div[class="push"] span')
                for info in push_info_list:
                    if '推' in info.text:
                        push_up += 1
                    if '噓' in info.text:
                        push_down += 1
                article_info_list = article_soup.select('div[class="article-metaline"] span')
                for n, info in enumerate(article_info_list):
                    if (n+1)%6 == 2:
                        author = info.text
                    if (n+1)%6 == 4:
                        title = info.text
                    if (n+1)%6 == 0:
                        datetime = info.text
                score = push_up - push_down
                article_content += '\n---split---\n'
                article_content += '推: %s\n'%(push_up)
                article_content += '噓: %s\n' % (push_down)
                article_content += '分數: %s\n'%(score)
                article_content += '作者: %s\n'%(author)
                article_content += '標題: %s\n'%(title)
                article_content += '時間: %s\n'%(datetime)
                with open('./{}/{}.txt'.format(resource_path, article_text), 'w', encoding='utf-8') as f:
                    f.write(article_content)
                print()
            except FileNotFoundError as e:
                print('==========')
                print(article_url)
                print(e.args)
                print('==========')
        except AttributeError as e:
            print('==========')
            print(each_article)
            print(e.args)
            print('==========')

    # url = 'https://www.ptt.cc' + soup.select('div[class="btn-group btn-group-paging"]')[0].select('a')[1]['href']
