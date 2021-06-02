import os
import pandas as pd
from urllib import request
from bs4 import BeautifulSoup


def get_http(url):
    request_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
    req = request.Request(url, headers = request_headers)
    try:
        res = request.urlopen(req)
        return res.read()
    except request.HTTPError as e:
        raise e
 
 
def get_page(page):
    url = 'http://kaijiang.zhcw.com/zhcw/inc/ssq/ssq_wqhg.jsp?pageNum=' + str(page)
    url_backup = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list_' + str(page) + '.html'
    print('load......', page, url)
    
    try: 
        content = get_http(url)
    except request.HTTPError: 
        try:
            print('trying......', page, url_backup) 
            content = get_http(url_backup)
        except request.HTTPError as e: 
            raise e
    
    soup = BeautifulSoup(content, features='lxml')
    em_list = soup.find_all('em')
    info_list = soup.find_all('td', {'align': 'center'})
    results = []
    n = 0; m = 0
    group = []; text = ''
    
    for ball in em_list:
        if n == 0:
            group.append(str(info_list[m+0].get_text()))
            group.append(str(info_list[m+1].get_text()))
        ball_num = str(ball.get_text())
        group.append(ball_num)
        n += 1

        if n == 7:
            group.append(text + ball_num)
            results.append(group)
            group = []
            text = ''
            n = 0; m += 5
        
        else:
            text += ball_num + ','
    
    return results


def get_history_result(out_file,maxi):
    results = []
    for i in range(1, int(maxi)+1):
        try:
            results += get_page(i)
        except Exception as e:
            print('error......', i, e)
    columns = {
        'date': str,
        'id': str,
        'r1': int,
        'r2': int,
        'r3': int,
        'r4': int,
        'r5': int,
        'r6': int,
        'b1': int,
        'summary': str
    }
    df = pd.DataFrame(columns=columns, data=results)
    os.chdir('/Users/ericzhou/Desktop/程序代码/Programming/Visual_Studio/Python/Projects/Lottery')
    df.to_csv(out_file, index=False, encoding='utf-8-sig')
    
    print('\nSaving......')
    print(df)
    return df

# def main():
#     get_history_result('data.csv')
# main()