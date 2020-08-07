import requests
from bs4 import BeautifulSoup
import re
import time
import traceback

def getHTML(url):
    headers = {
        'authority': 'weibo.cn',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.49',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cookie': 'SCF=AjnntoaCX-Y_eEN_kE9nWAWVgbgDY_jD2Bi5-a9OjlR43Qw-1Q_DR8oveHBhH-6g32THOG3nXX2-NkKzGEhZHMw.; SUB=_2A25yEE84DeRhGeNP41QV8S_EzTuIHXVR-1FwrDV6PUJbktANLU_hkW1NTk9FXg679p-2GqXQ3xwZ5cUNVVzADcm8; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5E0SIN25KcaEzfuONp--9J5JpX5K-hUgL.Fo-p1hqXeK2RSoM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMfeKncSh2p1hqN; SUHB=04WuvNgdU_Yi-0; ALF=1597754473; _T_WM=38edaedf50b31a8743ff5498485c92ab',
    }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return(r.text)
    except:
        return ''


def getInfo(html):
    soup = BeautifulSoup(html, 'lxml')
    for div in soup.body.contents[8]:
        try:
            text = div.span.get_text()
            pattern = r' (http|https|ftp)://t.cn/\w+'
            txt = re.sub(pattern, '', text)
            return(txt[:-25])
        except:
            continue


def weiboMain(dic):
    url = 'https://weibo.cn/topstcn?f=search_6'
    html = getHTML(url)
    result = getInfo(html)
    dic.update({'result': result})


def infoJudge():
    #time_ = int(input('请输入发送消息间隔秒数:'))
    time_ = 60
    weiboDict = {'result2': 'Hello World'}
    while True:
        try:
            now = time.strftime('[%H:%M:%S]')
            toWho = 'CSEC总台'
            weiboMain(weiboDict)
            if not weiboDict['result'] == weiboDict['result2']:
                weiboDict.update({'result2': weiboDict['result']})
                print(now, weiboDict['result2'])
                data = {"group_id": 853633006, "message": weiboDict['result2']}
                requests.post('http://localhost:5700/send_group_msg', data)
                with open('D:\\LogData.txt', 'a+') as f:
                    f.write(now+weiboDict['result2']+'\n')
            else:
                print(now, weiboDict['result2'])
                print('----发送过了---')
            time.sleep(time_)
        except:
            traceback.print_exc()
            continue
infoJudge()