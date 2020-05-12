#!/usr/bin/python3

import sys
import time
import requests
import csv
from bs4 import BeautifulSoup

print(sys.version)
print(sys.executable)
print(time.strftime("%d-%m-%Y %H:%M"))

name_time_file = time.strftime("%d_%m_%Y")

base_url_eng = 'https://www.cbr.ru/eng/currency_base/daily/'  # English site locale
base_url_ru = 'https://www.cbr.ru/currency_base/daily/'  # Russian site locale

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (HTML, like Gecko) '
                         'Chrome/79.0.3945.130 Safari/537.36'
           }

files = 'currency_' + name_time_file + '.csv'


def get_choice_base():
    print('Please select a site language. ENG -> 1; RU -> 2')
    global locale_site
    current_locale_url = False
    while not current_locale_url:
        choice_base_url = input('Enter a number: ')
        if int(choice_base_url) == 1:
            html_base_url = base_url_eng
            print('Site localization selected: English')
            locale_site = 'eng_'
            current_locale_url = True
        elif int(choice_base_url) == 2:
            html_base_url = base_url_ru
            print('Site localization selected: Russian')
            locale_site = 'ru_'
            current_locale_url = True
        else:
            print('WRONG DATA ENTERED!!! \n' 'Please select a site language. ENG -> 1; RU -> 2')
            continue
        return html_base_url


def get_html(base_url, params=None):
    session = requests.Session()
    request = session.get(base_url, headers=headers, params=params)
    return request


def get_current_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    current_data = soup.find_all('tr')
    if len(current_data) >= 35:
        return len(current_data)
    else:
        return len(current_data)


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find(class_='table-wrapper')

    global currency
    currency = []

    try:
        for item_tr in items('tr'):
            if item_tr.text:
                x = item_tr.text
                currency.append(x.strip().split("\n"))
            else:
                print(item_tr.img.get('src'))
        return currency
    except (RuntimeError, TypeError, NameError):
        print('Oops!  Something broke.  Try again...')


def save_data(currency, files):
    with open(files, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', dialect='excel')
        for line in currency:
            writer.writerow(line)


def parse_cbr():
    base_url = get_choice_base()
    html = get_html(base_url)
    if html.status_code == 200:
        current_data = get_current_data(html.text)
        if current_data >= 35:
            content_list = get_content(html.text)
            print(f'List of: {int((len(content_list) - 1)) }', 'currencies')
            save_data(currency, locale_site + files)
            print('Data saved to file:', locale_site + files)
        else:
            print('Oops! The list is not valid.', f'Actual:{current_data}; Expected:{34};')
    else:
        print('Error status code site:', html.status_code)


parse_cbr()
