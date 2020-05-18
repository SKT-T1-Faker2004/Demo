import os
import time
import ffmpy3
import requests
import colorama
from colorama import init
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool

init(autoreset=True)


#logo
print('=' * 40)
print('\n')
print('Movie Downloader | Ver. 1 (Special thanks to jusudhw.com)')
print('Modified by'+' \033[1;32;40m''EricZ')
print('Recent Update: 2020.05.17')
print('\033[1;31;43m''Do not spread for commercial purpose!')
print('=' * 40)
print('\n')

search_keyword = input('> 请输入关键字： ')
search_url = 'http://www.jisudhw.com/index.php'
serach_params = {
    'm': 'vod-search'
}
serach_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    'Referer': 'http://www.jisudhw.com/',
    'Origin': 'http://www.jisudhw.com',
    'Host': 'www.jisudhw.com'
}
serach_datas = {
    'wd': search_keyword,
    'submit': 'search'
}


video_dir = ''
    
r = requests.post(url=search_url, params=serach_params, headers=serach_headers, data=serach_datas)
r.encoding = 'utf-8'
server = 'http://www.jisudhw.com'
search_html = BeautifulSoup(r.text, 'lxml')
search_spans = search_html.find_all('span', class_='xing_vb4')
for span in search_spans:
    url = server + span.a.get('href')
    name = span.a.string
    print('=' * 40)
    print("搜索结果：" + name)
    print("在线观看地址，稍后将自动开始下载（较慢）：" + url)
    print('=' * 40)
    time.sleep(3)
    video_dir = name
    if name not in os.listdir('./'):
        os.mkdir(name)
        
    detail_url = url
    r = requests.get(url = detail_url)
    r.encoding = 'utf-8'
    detail_bf = BeautifulSoup(r.text, 'lxml')
    num = 1
    serach_res = {}
    for each_url in detail_bf.find_all('input'):
        if 'm3u8' in each_url.get('value'):
            url = each_url.get('value')
            if url not in serach_res.keys():
                serach_res[url] = num
            print('第%03d集:' % num)
            print(url)
            num += 1

def downVideo(url):
    num = serach_res[url]
    name = os.path.join(video_dir, '第%03d集.mp4' % num)
    ffmpy3.FFmpeg(inputs={url: None}, outputs={name:None}).run()
            
# 开8个线程池
pool = ThreadPool(8)
results = pool.map(downVideo, serach_res.keys())
pool.close()
pool.join()