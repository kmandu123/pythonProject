from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import pymysql

#210.114.22.108
#localhost
conn = pymysql.connect( host='210.114.22.108', user='root', password='Mysql801!', db='mycompanydb', charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

curs.execute("delete from books_best_book;")
conn.commit()


### 처리되는 화면 띄우기 아래와 둘중 하나로 처리되어야 함.
#driver = webdriver.Chrome('C:/Users/kmandu/chromedriver_win32/chromedriver.exe')

### batch처리를 위해 화면 구동 안함. -- start
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

driver = webdriver.Chrome('C:/Users/kmandu/chromedriver_win32/chromedriver.exe', chrome_options=options)
### batch처리를 위해 화면 구동 안함. -- end


url = 'http://www.kyobobook.co.kr/categoryRenewal/categoryMain.laf?perPage=20&mallGb=KOR&linkClass=01&menuCode=002'
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

books_data = []
rank = 1

books = soup.select('.info_area')  #li.id_detailli 의 하위 모든 요소들 중 div.detail을 찾겠다.

for book in books:
    book_name = book.select('div.title > a > strong')[0].text  # ‘>’ 의 의미 -> 바로 아래 요소 ‘.’다음에는 class명
    author_name = book.select('span.author')[0].text
    pub_name = book.select('span.publication')[0].text
    href = book.select('div.title > a')[0].attrs['href'] # a태그의 속성 href 값 가져오기
    book_href = 'http://www.kyobobook.co.kr/product/detailViewKor.laf?mallGb=KOR&ejkGb=KOR&linkClass=01&barcode={}'.format(href[37:50]) 
    book_info = book.select('div.info > span')[0].text
    image_info = book.select('.cover > a > span > img')[0].attrs['src'] 
    
    curs.execute("INSERT INTO books_best_book (site, genre, `rank`, book_name, author_name, publisher, book_url, book_info, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", ('교보문고', '소설', rank, book_name, author_name, pub_name, book_href, book_info, image_info))
    conn.commit()

    books_data.append(['교보문고','소설',rank,book_name,author_name,pub_name,book_href,book_info,image_info])
    rank = rank + 1

print('작업 완료')    

#columns = ['Site','분류', '순위','타이틀','작가','출판사','책URL','책정보', '이미지정보']
#pd_data = pd.DataFrame(books_data,columns=columns)
#pd_data
