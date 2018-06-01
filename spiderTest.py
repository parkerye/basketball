#coding:utf-8
'''
Created on 2016��5��17��

@author: jsjxy
'''
import urllib.request
import re
import ssl
from bs4 import BeautifulSoup
from distutils.filelist import findall



# This restores the same behavior as before.
context = ssl._create_unverified_context()

page = urllib.request.urlopen('http://map.baidu.com/detail?qt=ninf&uid=2b6ece311fcb48fee311038a&detail=life',context=context)
contents = page.read()
 #print(contents)
soup = BeautifulSoup(contents,"html.parser")
# print("豆瓣电影TOP250" + "\n" +" 影片名              评分       评价人数     链接 ")
# for tag in soup.find_all('div', class_='info'):
#    # print tag
#     m_name = tag.find('span', class_='title').get_text()
#     m_rating_score = float(tag.find('span',class_='rating_num').get_text())
#     m_people = tag.find('div',class_="star")
#     m_span = m_people.findAll('span')
#     m_peoplecount = m_span[3].contents[0]
#     m_url=tag.find('a').get('href')
#     print( m_name+"        "  +  str(m_rating_score)   + "           " + m_peoplecount + "    " + m_url )


for tag in soup.find_all('div', class_='partnernav'):
   # print tag
    m_url=tag.find('a').get('href')
    print(m_url)


for tag in soup.find_all('div', class_='netLink'):
   # print tag
    m_url=tag.find('a').get('href')
    print(m_url)

