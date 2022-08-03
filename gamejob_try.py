from __future__ import print_function
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.http import MediaFileUpload
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import  warnings
from    selenium import webdriver
from    selenium.webdriver.support.ui import WebDriverWait
from    selenium.webdriver.support import expected_conditions as EC
from    selenium.webdriver.common.by import By
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
from  pandas.core.frame import DataFrame
import  matplotlib.pyplot as plt
import  chromedriver_autoinstaller
import  subprocess
from    selenium import webdriver
from    selenium.webdriver.chrome.options import Options
from    selenium.webdriver.common.alert import Alert
import  chromedriver_autoinstaller
import  subprocess
import  shutil 
import  xlrd
import  openpyxl 
import  pygsheets
import  csv
import  re
import  webbrowser
import  os
import  sys
import  urllib.request
import  json
from    pandas.io.json import json_normalize
import  hashlib
import  hmac
import  base64
import  numpy as np
import  autoit #autoit는 반드시 autoit 프로그램이 깔려있어야됨
import  pyautogui
from PIL import ImageGrab

warnings.filterwarnings('ignore')

#게임잡 URL 불러오기

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
driver.maximize_window() #최대창
time.sleep(2)
driver.implicitly_wait(10)

url = 'http://www.gamejob.co.kr/Recruit/joblist?menucode=searchtot&searchtype=all&searchstring=분석'

driver.get(url)
#driver.maximize_window()  #창확대
action = ActionChains(driver)

#게임잡 URL 불러오기

f =  open('C:/Users/SAMSUNG/Desktop/python/raw/gamejob_apply.csv', 'w')
f.write("date,직무,URL"+'\n')

page = 0

for i in range(1, 5) :
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    job_lists = soup.find_all("div", class_='tit') #직무, URL
    for job_result in job_lists :
        job = job_result.find('a')
        job2 = job.get_text()
        url = "https://www.gamejob.co.kr" + job_result.find('a')['href'] 
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y-%m-%d')
        f.write(nowDate +','+job2 +','+url+'\n')
    try :
        page = page + 1
        driver.find_element_by_xpath('//*[@id="tab1"]/div/article/div/div/a[' + str(page)+ ']').click()
    except :
        print("수집완료, end")
        break
f.close()

# 데이터 쌓기

conn = pymssql.connect(server='localhost', user='pyuser', password='Dnflskfk12!', database='mytest' , charset='utf8')

gamejob_query = '''

IF OBJECT_ID(N'tempdb..#gamejob_apply') IS NOT NULL
DROP TABLE #gamejob_apply 

CREATE TABLE #gamejob_apply (
    Date date NULL,
    Job nvarchar(max) NULL,
    URL nvarchar(max)  NULL
)

bulk insert #gamejob_apply  from 'C:/Users/SAMSUNG/Desktop/python/raw/gamejob_apply.csv'  with (firstrow=2, fieldterminator = ',' , rowterminator = '\n', keepnulls )

insert into mytest.dbo.gamejob_apply
select * FROM #gamejob_apply 

select * FROM mytest.dbo.gamejob_apply with (nolock) ;
'''
data3 = pd.read_sql(sql=gamejob_query, con=conn)

conn.commit()
conn.close()

driver.close()
driver.quit()