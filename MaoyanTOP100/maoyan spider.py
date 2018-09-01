import requests
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
import time
import numpy as np
from multiprocessing import Pool

def get_one_page(url):

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):

    time.sleep(np.random.rand()*5)
    doc = pq(html)
    lists = doc('.content .main .board-wrapper dd').items()
    for list in lists:
        title = list.find('a').attr('title')
        stars = list.find('.board-item-main .star').text()[3:]
        releasetime = list.find('.board-item-main .releasetime').text()[5:]
        score1 = list.find('.board-item-main .score .integer').text()
        score2 = list.find('.board-item-main .score .fraction').text()
        score = score1+score2
        boardImg = list.find('a .board-img').attr('data-src')
        print(title,'<---->',stars,'<---->',releasetime,'<---->',score,'<---->',boardImg)
        

def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    parse_one_page(html)

if __name__ == '__main__':
    #引入多进程
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])


