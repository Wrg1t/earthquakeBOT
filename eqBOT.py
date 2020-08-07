import requests
from bs4 import BeautifulSoup
import re
import os
import time
import win32gui
import win32con
import win32clipboard as w

def getHTML(url):
    try:
        headers = {''}  # 自行获取header，因涉及cookies故删去
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
    #获取剪贴板文本
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return d


def setText(aString):
    #设置剪贴板文本
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
