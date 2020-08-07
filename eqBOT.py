import requests
from bs4 import BeautifulSoup
import re
import os
import time
import win32gui
import win32con
import win32clipboard as w

def getHTML(url):
    headers = {
        'authority': 'weibo.cn',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cookie': '_T_WM=2e729b5ceb497ba787ac8d7a16384b3d; SCF=AjnntoaCX-Y_eEN_kE9nWAWVgbgDY_jD2Bi5-a9OjlR43Qw-1Q_DR8oveHBhH-6g32THOG3nXX2-NkKzGEhZHMw.; SUB=_2A25yEE84DeRhGeNP41QV8S_EzTuIHXVR-1FwrDV6PUJbktANLU_hkW1NTk9FXg679p-2GqXQ3xwZ5cUNVVzADcm8; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5E0SIN25KcaEzfuONp--9J5JpX5K-hUgL.Fo-p1hqXeK2RSoM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMfeKncSh2p1hqN; SUHB=04WuvNgdU_Yi-0; ALF=1597754473',
    }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = ('utf-8')
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
    dic.update({'result':result})


def getText():
    """获取剪贴板文本"""
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return d


def setText(aString):
    """设置剪贴板文本"""
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()


def sendQQ(to_who, msg):
    # 将消息写到剪贴板
    setText(msg)
    # 获取qq窗口句柄
    qq = win32gui.FindWindow(None, to_who)
    # 投递剪贴板消息到QQ窗体
    win32gui.SendMessage(qq, 258, 22, 2080193)
    win32gui.SendMessage(qq, 770, 0, 0)
    # 模拟按下回车键
    win32gui.SendMessage(qq, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32gui.SendMessage(qq, win32con.WM_KEYUP, win32con.VK_RETURN, 0)


def infoJudge():
    time_ = int(input('请输入发送消息间隔秒数:'))
    weiboDict = {'result2':'Hello World'}
    while True:
        try:
            now = time.strftime('[%H:%M:%S]')
            toWho = 'CSEC总台'
            weiboMain(weiboDict)
            if not weiboDict['result'] == weiboDict['result2']:
                msg = weiboDict['result']
                print(now,weiboDict['result'])
                sendQQ(toWho,msg)
                weiboDict.update({'result2':weiboDict['result']})
            else:
                print(now,weiboDict['result2'])
                print('----发送过了---')
            time.sleep(time_)
        except:
            continue
infoJudge()