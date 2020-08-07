import requests
from bs4 import BeautifulSoup
import re
import time
import traceback

def getHTML(url):
    try:
        headers = {''}  # 自行获取header，因涉及cookies故删去
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
    time_ = int(input('请输入发送消息间隔秒数:'))
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
                requests.post('http://localhost:5700/send_group_msg', data)#coolq默认端口5700
                with open('LogData.txt', 'a+') as f:#在本地保存日志
                    f.write(now+weiboDict['result2']+'\n')
            else:
                print(now, weiboDict['result2'])
                print('----发送过了---')
            time.sleep(time_)
        except:
            traceback.print_exc()#debug用
            continue
infoJudge()