# -*- coding: utf-8 -*-

import sys
import requests
import time
from bs4 import BeautifulSoup
import io

KEYWORD = '口袋妖怪'
DEEP = 5
SEP = 'XYX'

def download_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return " ERROR "

def search_page(ID, title, author, date, rep_num):
    page_content = []
    
    page_url = 'https://tieba.baidu.com/p/' + str(ID)
    phtml = download_html(page_url)
    psoup = BeautifulSoup(phtml, 'lxml')
    
    li_reply = psoup.find_all('li', attrs={'class': 'l_reply_num'})[0]
    num_page = int(li_reply.find_all('span', attrs={'class': 'red'})[1].text.strip())
    
    reply = []
    
    for i in range(num_page):
        new_url = page_url + '?pn=' + str(i+1)
        new_html = download_html(new_url)
        new_soup = BeautifulSoup(new_html, 'lxml')
        # Space here
        # Change between clearfix
        divs_0 = new_soup.find_all('div', attrs={'class': 'd_post_content j_d_post_content ', 'style': 'display:;'})
        divs_1 = new_soup.find_all('div', attrs={'class': 'd_post_content j_d_post_content clearfix', 'style': 'display:;'})
        divs = divs_0 if len(divs_0) > len(divs_1) else divs_1
        
        comments = [div.text.strip() for div in divs]
        reply += comments
        
    for r in reply:
        page_content.append({'title': title, 'author': author, 'date': date, 'rep_num': rep_num, 'reply': r})
        
    return page_content

def search_content(url):
    content = []
    
    html = download_html(url)

    soup = BeautifulSoup(html, 'lxml')
    # Space here
    lis = soup.find_all('li', attrs={'class': ' j_thread_list clearfix'})

    for li in lis:
        try:
            title = li.find('a', attrs={'class': 'j_th_tit'}).text.strip()
            data_field = eval(li['data-field'].replace('null', 'None'))
            ID = data_field['id']
            author = data_field['author_name']
            date = li.find('span', attrs={'class': 'pull-right is_show_create_time'}).text.strip()
            rep_num = li.find('span', attrs={'class': 'threadlist_rep_num center_text'}).text.strip()
            
            content_new = search_page(ID, title, author, date, rep_num)
            content += content_new
            
            #print(title)
        except:
            #print('Error...')
            continue

    return content


def Out2File(keyword, file_dir, content, sep):
    with open(file_dir, 'a+', encoding = 'utf-8') as f:
        for comment in content:
            f.write('{}{}{}{}{}{}{}{}{}{}{}\n'.format(keyword, sep, comment['title'], sep, comment['author'], sep, comment['date'], sep, comment['rep_num'], sep, comment['reply']))

def ClearFile(file_dir, sep):
    with open(file_dir, 'w', encoding = 'utf-8') as f:
        f.write('{}{}{}{}{}{}{}{}{}{}{}\n'.format('tieba',sep, 'title',sep, 'author',sep, 'date',sep, 'rep_num',sep, 'reply'))


def main(keyword, deep, sep=SEP):
    file_dir = '../output/' + keyword + '.txt'
    
    base_url = 'https://tieba.baidu.com/f?kw=' + keyword + '&ie=utf-8'

    url_list = []
    ClearFile(file_dir, sep)
    content_pre = []
    n = 0

    for i in range(0, deep):
        url_list.append(base_url + '&pn=' + str(50 * i))
    print('Decoding htmls from 贴吧 {}吧'.format(keyword))
    
    for url in url_list:
        content_now = search_content(url)
        if content_now != content_pre:
            Out2File(keyword, file_dir, content_now, sep)
            n += 1
            print('Page #{} decoded'.format(n))
        else:
            break
        content_pre = content_now
    print('Finish')

if __name__ == '__main__':
    keyword = KEYWORD
    deep = DEEP
    main(keyword, deep)