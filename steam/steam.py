import requests
from bs4 import BeautifulSoup
import re
import time
import pymysql.cursors
from urllib.parse import urlencode


#获取数据库连接
connection = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'hyx.5899360',
    db = 'steaminfo',
    charset = 'utf8mb4')


def getHTMLText(url,k):
    try:
        if(k==0):
            params={'filter':'topsellers'}
        else:
            params={
                'filter':'topsellers',
                'page':k+1
                }
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'}
        url = basic_url + urlencode(params)
        r = requests.get(url,headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('Failed！')

        
basic_url = 'https://store.steampowered.com/search/?'

k = 0
while k < 2:
    html = getHTMLText(basic_url, k)
    time.sleep(5)
    k = k+1

    soup = BeautifulSoup(html, 'html.parser')

    gameList = soup.find('div',id='search_results')
    for a in gameList.findAll('a',href=re.compile(r'^(https://store\.steampowered\.com)')):
        if not re.search('/search/',a['href']):
            href = a['href']
            info = a.find('div', class_='responsive_search_name_combined')
            name = info.find('span',class_='title').get_text()
            date = info.find('div',class_='col search_released responsive_secondrow').get_text()
            if date == '':
                date = "no data"
            price_info = info.find('div',class_='col search_price_discount_combined responsive_secondrow')
            p = re.findall(r'-?\d+%?',str(price_info))
            if len(p) > 1:
                price_s = p[-2]
                discount = p[-4]
                price = p[-1]
            else:
                price_s = p[0]
                discount = 0
                price = p[0]

            # print(name,'<---->',date,'<---->',href,'<---->',price_s,'<---->',discount,'<---->',price)
            

            cursor = connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS steam")

            #创建数据表
            sql = '''CREATE TABLE steam (
                     id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                     gamename VARCHAR(50) NOT NULL,
                     gamedate VARCHAR(20) NOT NULL,
                     gamehref VARCHAR(255) NOT NULL,
                     gameprice_s FLOAT(6,0) NOT NULL,
                     gamediscount VARCHAR(20) NOT NULL,
                     gameprice FLOAT(6,0) NOT NULL )'''
            cursor.execute(sql)

            sql = 'INSERT INTO `steam`(`gamename`,`gamedate`,`gamehref`,`gameprice_s`,`gamediscount`,`gameprice`) VALUES(%s,%s,%s,%s,%s,%s)'
            result=(name,date,href,price_s,discount,price)
            cursor.execute(sql,result)
            connection.commit()
            #cursor.close()   游标关闭
            #connection.close()   连接关闭

    print("完成%s页" %k)


