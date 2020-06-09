from urllib import parse
import requests
from bs4 import BeautifulSoup as bs
import webbrowser
import colorama
from colorama import init

init(autoreset=True)

print('+' + '-' * 40 + '\n' )
print('Made by EricZ\n2020.06.09')
print('Sepcial Thanks to \'Anypaper.com\'\n')
print('\033[1;31;43m''DO NOT USE FOR COMMERCIAL PURPOSE')
print('+' + '-' * 40 + '\n' )

url_raw = input('> 请输入文章网址: ')
url_encoded = parse.quote(url_raw)

print('\n[+] Opening...')

link = 'https://ifish.fun/paper/search?key='+url_encoded

header={
  'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
}

r = requests.get(link, headers=header)
html = r.content
soup = bs(html, 'html.parser')
article_link = soup.find(['u'])

article = article_link.get_text()

webbrowser.open_new(article)

print('\n[+] Opened. Quiting...')