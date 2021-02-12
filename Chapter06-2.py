from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime

from selenium import webdriver
import time


#크롬 WebDriver객체생성
wd = webdriver.Chrome('C:\\Users\\LG\\Documents\\phython_hwang\\HwangGlasses2_BigData\\WebDriver\\chromedriver.exe') 

wd.get("https://www.coffeebeankorea.com/store/store.asp") #웹페이지연결
wd.execute_script("storePop2(1)") #1번매장 지점의 정보가 팝업창으로 나타남

html = wd.page_source #자바스크립트 함수가 수행된 페이지 소스코드를 저장
soupCB1 = BeautifulSoup(html, 'html.parser') #BeautifulSoup 객체 생성
#print(soupCB1.prettify()) #HTML 소스코드 형태로 출력

#매장이름추출
store_name_h2 = soupCB1.select("div.store_txt > h2")
store_name_h2
#store_name = store_name_h2[0].string
#store_name

#오류생겨서 추가
#raise new_exc from original_exc
