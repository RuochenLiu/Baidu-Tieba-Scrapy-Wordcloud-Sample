import sys
import requests
import time
from bs4 import BeautifulSoup
import io
import json
import re
import pandas as pd
import numpy as np
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

cookie_choice = ['apple', 'microsoft', 'pachama', 'sony', 'tencent']
user_agent_list = [
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
                    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
                    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
                    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
                    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
                    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
                ]

COOKIE_NUMBER = 0
cook = ''

def download_html(url):
    global COOKIE_NUMBER
    global cook

    if COOKIE_NUMBER % 10 == 0:
        browser = webdriver.Chrome()
        new_cookie = random.choice(cookie_choice)
        # print('Cookie from '+new_cookie+'\n')
        browser.get('https://www.crunchbase.com/organization/'+new_cookie)
        Cookie = browser.get_cookies()
        cook = ''
        for c in Cookie:
            cook += c['name']
            cook += '='
            cook += c['value']
            cook += ';'
    
    print(cook)
    COOKIE_NUMBER += 1

    try:
        new_ua = random.choice(user_agent_list)
        # print('User-Agent as '+new_ua+'\n')
        headers = {
                    'user-agent': new_ua,
                    'cookie': cook
                }
        r = requests.get(url, headers=headers, cookies={'from-my': 'browser'}, timeout=100)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return " ERROR "
    
def get_founded_year(psoup):
    # Founded Year
    try:
        status = [x.text.strip() for x in psoup.find_all('span', attrs={'class': 'component--field-formatter field-type-enum ng-star-inserted'})]
    except:
        res = 'Unknown'
    
    try:
        index = 1 if 'Closed' in status else 0
        res = psoup.find_all('span', attrs={'class': 'component--field-formatter field-type-date_precision ng-star-inserted'})[index].text.strip()
        res = res[-4:]
    except:
        res = 'Unknown'
    
    return res

def get_category(psoup):
    # Industries
    try:
        res = [x.text.strip() for x in psoup.find_all('mat-chip', attrs={'role': 'option'})]
    except:
        res = 'Unknown'
    return res

def get_last_fund(psoup, lower_company):
    try:
        res = psoup.find_all('a', attrs={'href': '/search/funding_rounds/field/organizations/last_funding_type/'+lower_company})[0].text.strip()
    except:
        res = 'Unknown'
    return res

def get_description(psoup):
    try:
        res = psoup.find_all('meta', attrs={'name': 'description'})[0]["content"]
    except:
        res = 'Unknown'
    return res

def get_info(company_name):
    home_page = 'https://www.crunchbase.com/organization/'
    lower_company = company_name.lower()
    page_url = home_page + lower_company
    phtml = download_html(page_url)
    psoup = BeautifulSoup(phtml, 'html.parser')
    return get_founded_year(psoup), get_category(psoup), get_last_fund(psoup, lower_company), get_description(psoup)

def print_info(company_name):
    r = get_info(company_name)
    print('\n{}\nFounded: {}\nIndustry: {}\nLast Fund: {}\n'.format(company_name, r[0], ', '.join(r[1]), r[2]))

def generate_csv(source):
    founded_year = []
    industry = []
    last_fund = []
    desc = []
    company_list = source.CompanyName
    total = len(company_list)
    processed = 0
    start = 1
    end = total
    number = end-start+1
    for i in range(start-1, end):
        company = company_list[i]
        company = company.replace(' ', '-').replace('.', '-')
        res = get_info(company)
        print('\n{}\nFounded: {}\nIndustry: {}\nLast Fund: {}\nDesc: {}\n'.format(company, res[0], ', '.join(res[1]), res[2], res[3]))
        time.sleep(random.choice([0.2, 0.1, 0.3]))
        founded_year.append(res[0])
        industry.append(res[1])
        last_fund.append(res[2])
        desc.append(res[3])
        processed += 1
        print('#### Processed {}/{} ####\n'.format(processed, number))
        # print('Processing {0:.1f}% ...'.format(processed/total*100), end='\r')
    print('\nSaving to CSV file ...')
    data = {'CompanyName': company_list[start-1:end], 'FoundedYear': founded_year, 'Industry': industry, 'LastFund': last_fund, 'Desc': desc}
    df = pd.DataFrame(data, columns=['CompanyName', 'FoundedYear', 'Industry', 'LastFund', 'Desc'])
    df.to_csv('../output/output.csv', index=0)

def main():
    source = pd.read_csv('../data/Com.csv')
    generate_csv(source)

if __name__ == "__main__":
    main()