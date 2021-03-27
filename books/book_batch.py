from selenium import webdriver
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import pandas as pd
import time
import pymysql

conn = pymysql.connect( host='210.114.22.108', user='root', password='Mysql801!', db='mycompanydb', charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)
curs.execute("select * from books_author;")
result = curs.fetchall()

curs.execute("delete from books_author_book;")
conn.commit()

for r in result:
    author_info = r['author_name']
#    print(author_info)



#    driver = webdriver.Chrome('C:/Users/kmandu/chromedriver_win32/chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome('C:/Users/kmandu/chromedriver_win32/chromedriver.exe', chrome_options=options)
    
    
    
    
    url = 'http://www.yes24.com/searchcorner/search/DetailCondition?domain=BOOK'
    driver.get(url)

    time.sleep(2)

    #작가 입력
    author = author_info
    input_id = driver.find_elements_by_css_selector('#dscBOOK_Author')[0]
    input_id.clear()
    input_id.send_keys(author)

    time.sleep(1)

    #버튼 클릭
    btn = '#btnDetailCondition'
    driver.find_element_by_css_selector(btn).click()
    time.sleep(1)

    #신상품 클릭
    link = '#formTest > ul > li:nth-child(3) > a'
    driver.find_element_by_css_selector(link).click()
    time.sleep(2)

    #도서 정보 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(3)

    #20개 도서목록 정보 추출하기
    books_info = soup.select('.goods_infogrp')
    image_info = soup.select('td.goods_img > a > img')
    #print(len(image_info)) #확인
    #print(image_info[0]) #확인

    
    #20개 도서목록 정보에서 필요한 정보만 looping처리하면서 추출하기
    book_list=[]
    i = 0

    for item in books_info:    
        book_name = item.select('strong')[0].text.strip()
        pub_date = item.select('td.goods_infogrp > div.goods_info > em')[0].text
        img_url = str(image_info[i])
        i += 1
        print(author, book_name,pub_date,img_url)
        
        curs.execute("INSERT INTO books_author_book (author_name, book_name, pub_date, image_url) VALUES (%s, %s, %s, %s)", (author, book_name, pub_date, img_url)) 
        conn.commit()
