# -*- coding: UTF-8 -*-
from urllib import request
import requests
import urllib
import time 
from lxml import etree
import re
import json
#
#
#请求 URL: http://www.5nd.com/paihang/tuijiangequ.htm
#http://mpge.5nd.com/2020/2020-6-15/97048/1.mp3   单手歌曲的下载地址
#<div class="songPlayBox"><div id="kuPlayer" data-play="2020/2020-6-15/97048/1.mp3"></div>

#<script type="text/javascript"> var urlht = "2020/2020-6-15/97048/1.mp3";</script>

songId=[]
songName=[]
singerName=[]
lrc_id = []
url="http://www.5nd.com/paihang/tuijiangequ.htm"
headers={
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363"
}
try:

    response=requests.get(url,headers=headers).content.decode('gb2312','ignore')
    #print(response)
except Exception as e:
    print(e)
#print(response)
#解析网页获取所需信息

pat=re.compile('<a target="_ting" href="(.*?)"')
data1=pat.findall(response)   
# 这个为歌曲的songid  可以得到每首音乐的地址
# http://www.5nd.com/ting/661821.html

html=etree.HTML(response)
hdata=html.xpath('//a[@class="rankNane"]')
for j in range(len(hdata)):
    if j <=1000:
        song=hdata[j].text.split("-")[0]
        singer=hdata[j].text.split("-")[1]
        #打印歌曲名称-----------
        #print(song)
        #print(singer)
        # print(song)
        songName.append(song)     # 获得歌曲名称
        singerName.append(singer)   #  获得歌手名字
#print(data1[0])

# print(songName)
for i in range(len(data1)):
    #http://www.5nd.com/ting/660473.html
    if i<=1000:
        # lrc_id.append(data1[i])
        myurl="http://www.5nd.com"+data1[i]
        print(myurl)
        response2=requests.get(myurl,headers=headers).text 
        pat2=re.compile('id="kuPlayer" data-play="(.*?)">')
        data2=pat2.findall(response2)
        #print(type(data2))
        #print(len(data2))
        songId.append(data2[0])   # 歌曲的播放地址id


print(songId)  
for x in range(0,len(songId)):  # 下载歌曲并保存e://music
    print(x+1)
    playurl="http://mpge.5nd.com/"+songId[x]
    print(playurl)
    
    data=requests.get(playurl,headers=headers).content
    #print(data)
    print("正在下载第"+str(x+1)+"首歌曲")
    sn=songName[x]
    print(sn)
    with open("E:\\music\\{}.mp3".format(sn),"wb") as f:
        f.write(data)
        time.sleep(0.5)

for x in range(0,len(songId)): # 下载歌词在e://music_lrc中
    if x<1000:
        print(x+1)
        pk = data1[x].split('/')[2].split('.')[0] # 提取url中的660473数值 拼接歌词url
        print(pk)
        # 歌词url地址从分析中可以得知
        lrc_url = 
        'http://geapi.5nd.com/a/ar5bc.ashx?_c=mtest&_p=bXRlc3Q&nd=getSong&t=100&_lrc=1&ids={}'.format(pk)
        print(lrc_url)
        data=requests.get(lrc_url,headers=headers).content.decode()
        
        # print(data)  获取网页内容
        lrc_pattern=re.compile('"lrc":"(.*?)"')
        # 利用正则简单提取歌词
        #print(data)
        lrc=lrc_pattern.findall(data)[0].replace('\\n','\n')   
        # 这一步很重要，不然会出现控制台输出含\n换行符，保存的歌词不换行！！！！
        # 原理里：当控制台显示中含\n字符串时，得到歌词内容的原数据是为\\n形式的
        # 只有将\\n替换成\n后，在控制台显示的内容才会换行，并且当保存到文件中时，歌词自动换行
        # 这个困扰了我很长时间，想通了原理才解决！！！
        # print('这首歌的歌词是：',type(lrc))
        print(lrc)
        sn=songName[x]
        print(sn)
    
        with open("E:\\music_lrc\\{}.lrc".format(sn),'w') as f:
            f.write(lrc)
        
'''
# http://geapi.5nd.com/a/ar5bc.ashx?_c=mtest&_p=bXRlc3Q&nd=getSong&t=100&_lrc=1&ids=661821
# 音乐歌词地址的url
# http://geapi.5nd.com/a/ar5bc.ashx?_c=mtest&_p=bXRlc3Q&nd=getSong&t=100&_lrc=1&ids=661640 
#  获得歌词的地址  
#             
# album_id: 97759
# album_name: "Rock二人转"
# fav: 0
# location: "2020/2020-8-21/97759/1.mp3"
# lrc: "[00:01.89]Rock二人转↵[00:03.31]词/曲：刘凤瑶↵[00:04.71]..."
# lrc_type: 1
# singer_id: 29187
# singer_name: "朱烁燃（朱杰）"
# song_id: 661821
# song_name: "Rock二人转"
# song_status: 1
'''
