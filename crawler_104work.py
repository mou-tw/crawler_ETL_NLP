#-*-coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests ,os,json,re,jieba,time
import pandas as pd
import xlsxwriter

columns=['公司名稱','工作名稱','工作網址','工作內容','薪水','工作經歷','學歷','科系','其他條件']
with open('./appendind_list/appending_skill.txt', 'r', encoding='utf-8') as f:
    columns =columns + f.read().split('\n')

headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

same_mean_list=[]
with open('./same_meaning_list/same_meaning.txt','r',encoding='utf-8') as f:
    list =f.read().split('\n')
for eachlist in list:
    same_mean_list.append([item.replace('\ufeff','') for item in eachlist.split(',')])


def get_detail(keyword):
    titlelist ,urllist =[],[]
    page_count = 1
    while True:
        url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={}&order=15&asc=0&page={}&mode=s'.format(keyword,page_count)
        res = requests.get(url , headers = headers)
        soup = BeautifulSoup(res.text , 'html.parser')
        job_title_list = soup.select('h2[class="b-tit"] a')
        for jobs in job_title_list:
            if 'javascript' not in jobs['href']:
                titlelist.append(jobs.text)
                urllist.append(jobs['href'].replace('//','https://'))
        page_count += 1
        if len(job_title_list) < 20:
            break
    return titlelist ,urllist

def word_clean(str):
    for w_list in same_mean_list:
        for word in w_list:
            if word.upper() in str.upper():
                # print(w_list[0])
                if word.upper() == 'JAVA' or word.upper() =='JAVASCRIPT':
                    continue
                elif  word.upper() =='R' and 'R' in re.compile('( [\W]+R[\W]+)').findall(str):
                    str = re.sub(re.compile('([\W]+R[\W]+)'), 'R語言', str)
                else:
                    str = str.replace(word.upper(), w_list[0])
    return str

def skill_count(str):

    with open('./skillcount_list/skillcount.txt', 'r', encoding='utf-8') as f:
        skillCount_list = (f.read().split('\n'))

    count_dict = {}

    jieba.load_userdict('./wordlist/wordlist.txt')
    word_list = jieba.cut(str.upper())
    for word in word_list:
        if word in count_dict:
            count_dict[word] += 1
        else:
            count_dict[word] = 1
    tmp_dict={}
    for skill in skillCount_list:
        skill =skill.upper()
        if skill in count_dict:
            tmp_dict[skill] = count_dict[skill]

    count_list = [(k,tmp_dict[k]) for k in tmp_dict]
    count_list.sort(key=lambda x: x[1], reverse=True)
    return count_list

def skillAppend(str):
    skillGet_list=[]
    sub_str = word_clean(str)
    with open('./appendind_list/appending_skill.txt','r',encoding='utf-8') as f:
        apdSkill_list = f.read().split('\n')

    #新增進columns
    for i in apdSkill_list:
        if i.replace('\ufeff','').upper() in sub_str.upper():
            skillGet_list.append('○')
        else:
            skillGet_list.append('X')

    return skillGet_list



def req_job_page(urllist):
    tmp_list,combine_list=[],[]
    tmp_str = ''
    c=0
    for job in urllist:
        job_attr = job.split('/')[-1].split('?')[0]  # 各別網頁參數
        jobres_url = 'https://www.104.com.tw/job/ajax/content/' + job_attr  # res網址
        headers["Referer"] = "https://www.104.com.tw/job/" + job_attr
        # 擷取各工作關鍵網頁參數，帶入headers，並修改url
        job_res = requests.get(jobres_url, headers=headers)
        j = json.loads(job_res.text)

        company_name = j['data']['header']['custName']
        job_name = j['data']['header']['jobName']
        job_url = job
        job_content = j['data']['jobDetail']['jobDescription']
        salary = j['data']['jobDetail']['salary']
        work_exp = j['data']['condition']['workExp']
        education = j['data']['condition']['edu']
        major = j['data']['condition']['major']
        other = j['data']['condition']['other']
        # 將資訊放入list中，預備放入DATAFRAME
        # tmp_list.append([company_name, job_name, job_url, job_content, salary, work_exp, education, major, other])
        tmp_list=[company_name, job_name, job_url, job_content, salary, work_exp, education, major, other]
        # 新建一字串，由content和other組成
        tmp_str += (job_content+ other)
        skill_list = skillAppend(job_content+other)
        combine_list.append(tmp_list+skill_list)
        c+=1
        print('done job{}'.format(c))
    return combine_list ,tmp_str


def main():
    keyword = '爬蟲'
    t = time.strftime("%Y-%m-%d_%H%M")
    job_title, job_url =get_detail(keyword)
    job_list , content_str = req_job_page(job_url)

    skillCountlist = skill_count(content_str)

    # print(job_list)
    print('=======')
    print(skillCountlist)
    df = pd.DataFrame(columns=columns)
    df = df.append(pd.DataFrame(job_list, columns=columns))

    #save
    if not os.path.exists('test104'):
        os.mkdir('test104')
    df.to_excel(r'./test104/{}_{}.xlsx'.format(keyword,t),index=None, encoding='utf-8', engine='xlsxwriter')

    with open('./test104/{}_{}.txt'.format(keyword,t),'w' , encoding='utf-8' ) as f:
        f.write(str(skillCountlist))
    print('done_save')





if __name__ =='__main__':
    main()