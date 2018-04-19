#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-12 22:05:02
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import os
import sys
import json
import time
from pprint import pprint
import requests
from lxml import html
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
import getpass
from random import randint

LOGIN_PAGE_URL = 'https://weblogin.umich.edu/'
LOGIN_POST_URL = 'https://weblogin.umich.edu/cosign-bin/cosign.cgi'
HOUSING_PAGE_URL = 'https://studentweb.housing.umich.edu'
APARTMENT_SELECTION_PAGE_URL = 'https://studentweb.housing.umich.edu/SelectRoom.asp?Function=6952'
SEARCH_ROOM_URL = 'https://studentweb.housing.umich.edu/SelectRoomResults.asp'

HOUSING_PATE_SECTION_TEXT = 'Graduate and Family Residences 2018-2019'
NO_RESULT_TEXT = 'There are no rooms available that match your search.'

session_requests = requests.session()

def send_sms(msg, _mail_to):
    ACCOUNT_SEND = '171517787@qq.com'
    ACCOUNT_PWD = 'gzrfjeyqvkibcbdg'
    SEND_TO = _mail_to
    
    mail = MIMEText(msg)
    mail['From'] = formataddr(["FromRunoob",ACCOUNT_SEND])
    mail['To'] = formataddr(["FK",SEND_TO])
    mail['Subject'] = 'Regarding UM-Housing'
    
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(ACCOUNT_SEND, ACCOUNT_PWD)
    server.sendmail(ACCOUNT_SEND,[SEND_TO,],mail.as_string())
    server.quit()

def extract_info_from_html_elems(elems):
    # Cut table header
    elems = elems[1:]

    departments = []
    for elem in elems:
        vals = elem.cssselect('td')
        vals[0] = vals[0].cssselect('a')[0]

        department = {
            'Name': vals[0].text,
            'Area': vals[1].text,
            'Apartment Type': vals[2].text,
            'Contract Start Date': vals[3].text,
            'Square Footage': vals[4].text,
            'Environment': vals[5].text,
            'Air Conditioning': vals[6].text,
            'Furniture Type': vals[7].text,
            'Bedroom Dimensions': vals[8].text,
            'Available Space': vals[9].text
        }

        departments.append(department)

    return departments


def search():
    payload = {
        #'fld24526': 49,  # Ready to process: {49(Yes)}
        'fld28053': 'Unfurnished',  # Furnishings: {Furnished, Unfurnished}
        'fld28051': 'August 1',  # Contract start date: {July 1, July 16, August 1, August 16, September 1, September 16}
        'dateflddtArrival': '8/1/2018',  # Arrival date: %-m/%-d/%Y (e.g., 8/15/2017)
        'dateValueflddtArrival': '',
        'fldFunction': 6952,
        'btnSubmit': 'Search',
        'fld28052': 49,
        #'chkRoommate134660':'on'
    }

    session_requests.get(APARTMENT_SELECTION_PAGE_URL)

    print('Search')
    result = session_requests.post(
        SEARCH_ROOM_URL, data=payload)

    if result.status_code / 100 != 2:
        print('Failed')
        return None

    if result.text.find(NO_RESULT_TEXT) != -1:
        # No result
        print('No result')
        return None

    # Parse html file
    tree = html.fromstring(result.text)

    # Select apartment list
    elems = tree.cssselect('table.DataTable tr')

    # Check the number of elements (at lease one row)
    if len(elems) < 1:
        # No result
        print('No result (false positive)')
        return None

    # Extract from html elements
    departments = extract_info_from_html_elems(elems)

    print('Results!')
    return departments


def login(username, password):
    payload = {
        'ref': '',
        'service': '',
        'required': '',
        'login': username,
        'password': password
    }

    # Get cookie
    print('Get cookie')
    result = session_requests.get(LOGIN_PAGE_URL)
    if result.status_code / 100 != 2:
        print('Failed')
        return False

    # Login
    print('Login')
    result = session_requests.post(
        LOGIN_POST_URL, data=payload)
    if result.status_code / 100 != 2:
        print('Failed')
        return False

    # Check login
    print ('Housing')
    result = session_requests.get(HOUSING_PAGE_URL)

    if result.status_code / 100 != 2:
        print('Failed')
        return False

    print ('Finding')
    if result.text.find(HOUSING_PATE_SECTION_TEXT) == -1:
        print('Failed')
        return False

    return True

def main():

    username = raw_input('Uniqname: ')
    while username.strip() == '':
      print >> sys.stderr, 'Uniqname cannot be empty.'
      username = raw_input('Uniqname: ')
    pwd = getpass.getpass()
    _mail_to = raw_input('Email address: ')

    send_sms('Automatic msg from Python - Start searching', _mail_to)
    
    cnt = 0
    if login(username, pwd):
        while True:
            departments = search()

            if departments is not None:
                pprint(departments)

                simple_info = [(
                    '%s (Space: %s)' % (
                        department['Name'],
                        department['Available Space'])) for department in departments]

                send_sms('NORTHWOOD!!!!!!!' + '\n'.join(simple_info), _mail_to)

                print('Sleeping certain seconds...')
                time.sleep(randint(3, 20))
                return 0
            else:
                print('Sleeping certain seconds...' + str(cnt))
                time.sleep(randint(3, 20))
            cnt += 1
    else:
        print('Please check your uniqname and password.')


if __name__ == '__main__':
    main()
