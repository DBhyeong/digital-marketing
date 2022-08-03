#!/usr/bin/env python
# coding: utf-8

# In[1]:


import  warnings
from    selenium import webdriver
from    selenium.webdriver.common.keys import Keys 
from    selenium.webdriver.common.action_chains import ActionChains
from    selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from    bs4      import BeautifulSoup
import  time
import  pyperclip
import  requests
import  datetime
import  pymssql
import  pandas as pd
import  chromedriver_autoinstaller
import  subprocess

# !pip install chromedriver_autoinstaller <-- 주피터에선 ! 붙이면은 설치됨.

# date, 회사, 직무, URL
#'https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk=' + 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import shutil

warnings.filterwarnings('ignore')

f =  open('C:/Users/SAMSUNG/Desktop/python/raw/indeed_apply.csv', 'w', encoding='utf-8-sig')
f.write("date,회사,직무,URL"+'\n')

try:
    shutil.rmtree(r"c:\chrometemp")  #쿠키 / 캐쉬파일 삭제
except FileNotFoundError:
    pass

subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동

option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
driver.implicitly_wait(10)

for n in range(0, 1001, 50) :
    url = 'https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D&limit=100&radius=25&start=' + str(n)
    driver.get(url)
    driver.implicitly_wait(10)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all("a", {"class" : "tapItem"})
    for ar in results :
        title = ar.find("h2", {"class" : "jobTitle"}).select_one("span[title]").text
        title2 = title.replace(",", "")
        try : 
            company = ar.find("span", {"class" : "companyName"}).text
        except :
            company = "회사명없음"
        url = ar.attrs['data-jk']
        url2 = 'https://kr.indeed.com/viewjob?jk=' + str(url)
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y-%m-%d')
        f.write(nowDate + ',' + str(company) + ',' + str(title2) +',' + str(url2) + '\n')
        
f.close()        
driver.close()

# 데이터 쌓기

conn = pymssql.connect(server='localhost', user='pyuser', password='Dnflskfk12!', database='mytest' , charset='utf8')

indeed_query = '''

IF OBJECT_ID(N'tempdb..#indeed_apply') IS NOT NULL
DROP TABLE #indeed_apply 

CREATE TABLE #indeed_apply (
    Date date NULL,
    Company nvarchar(max) null, 
    Job nvarchar(max) NULL,
    URL nvarchar(max)  NULL
)

bulk insert #indeed_apply  from 'C:/Users/SAMSUNG/Desktop/python/raw/indeed_apply.csv'  with (firstrow=2, fieldterminator = ',' , rowterminator = '\n', codepage='65001' , keepnulls )

insert into mytest.dbo.indeed_apply
select * FROM #indeed_apply 

select * FROM mytest.dbo.indeed_apply with (nolock) ; 
'''
data3 = pd.read_sql(sql=indeed_query, con=conn)

conn.commit()
conn.close()


# In[ ]:




