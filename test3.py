#coding:utf-8
import requests
import json
import pymysql
import time
from datetime import datetime


city_list=[]
with open('cities.txt','r') as f:
    for eachline in f:
        if eachline !='' and eachline !='\n':
            city=eachline.split('\t')[0]
            city_list.append(city)
    f.close()


def getjson(palace,page_num=0):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        url='http://api.map.baidu.com/place/v2/search'
        params={
            'q':"篮球场",
            'region':palace,
            'scope':'2',
            'page_size':'20',
            'page_num':page_num,
            'output':'json',
            'ak':'XM53LMurtNQaAPFuKVy1WzSyZCNmNA9H',
        }
        response=requests.get(url=url,params=params,headers=headers)
        html=response.text
        decodejson=json.loads(html)
        #print(decodejson)
        print "successful1"
        return decodejson
    except:
        print "fail1"
        pass



def getuidjson(uid):
    try:
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        params={
            'uid':uid,
            'scope':'2',
            'output':'json',
            'ak':'XM53LMurtNQaAPFuKVy1WzSyZCNmNA9H',
        }
        url='http://api.map.baidu.com/place/v2/detail'
        response=requests.get(url=url,headers=headers,params=params)
        html=response.text
        decodejson=json.loads(html)
        print "successful2"
        return decodejson
    except:
        print "fail2" 
        pass



conn=pymysql.connect(host='127.0.0.1',user='root',password='root',db='court',charset='utf8')
cur=conn.cursor()
city_num=0
for city in city_list:
    not_last_page=True
    page_num=0
    city_num=city_num+10000
    court_num=1
    while not_last_page:
        decodejson=getjson(city,page_num)
        #print(city,page_num)
        if decodejson.get('results'):
            for result in decodejson.get('results'):
                time.sleep(5)
                Id=city_num+court_num
                uid=result.get('uid')

                decodejson=getuidjson(uid)
                data=decodejson.get('result')
                #print data
                if data:
                    park=data.get('name')
                    location_lat = data.get('location').get('lat')
                    location_lng=data.get('location').get('lng')
                    address=data.get('address')
                    street_id=data.get('street_id')
                    telephone=data.get('telephone')
                    detail=data.get('detail')
                    uid=data.get('uid')
                    tag=data.get('detail_info').get('tag')
                    detail_url=data.get('detail_info').get('detail_url')
                    type=data.get('detail_info').get('type')
                    overall_rating=data.get('detail_info').get('overall_rating')
                    image_num=data.get('detail_info').get('image_num')
                    comment_num=data.get('detail_info').get('comment_num')
                    shop_hours=data.get('detail_info').get('shop_hours')
                    alias=data.get('detail_info').get('alias')
                    scope_type=data.get('detail_info').get('scope_type')
                    scope_grade=data.get('detail_info').get('scope_grade')
                    description=data.get('detail_info').get('description')
                    print detail_url
                    sql="""INSERT INTO court.park(Id,park,location_lat,location_lng,address,street_id,telephone,detail,uid,tag,type,overall_rating,image_num,comment_num,shop_hours,alias,scope_type,scope_grade,description,time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
                    cur.execute(sql,(Id,park,location_lat,location_lng,address,street_id,telephone,detail,uid,tag,type,overall_rating,image_num,comment_num,shop_hours,alias,scope_type,scope_grade,description,datetime.now()))
                    conn.commit()
                court_num=court_num+1
            page_num=page_num+1
        else:
            not_last_page=False
        time.sleep(5)
cur.close()
conn.close()
