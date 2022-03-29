#%%
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from urllib import request

import time
import os
import datetime
import sys
import base64
import re
import ssl

#%%
search_word = "공룡"

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('에러 : 폴더 만들기 실패 ' +  directory)
        sys.exit()

# 기본 폴더 생성 (현재 디렉토리 아래 '구글이미지'디렉토리 생성)
att_base = './구글이미지(첨부파일)'
createFolder(att_base)

# 실행 시점 기반 폴더 생성 ('구글이미지'디렉토리 아래 '오늘날짜_시간분' 폴더 생성)
today = str(datetime.datetime.today())[0:16].replace("-", "").replace(" ", "_").replace(":", "")
att_folder = f'{att_base}/{today}/'
createFolder(att_folder)

#%%

# SSL 에러 우회 : 이미지 다운로드 시 [SSL: CERTIFICATE_VERIFY_FAILED] 에러 발생 
ssl._create_default_https_context = ssl._create_unverified_context

#opener=request.build_opener()
#opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36')]
#request.install_opener(opener)

opt = Options()

opt.add_argument('--start-maximized')
opt.add_argument('User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"')
# 로봇 크롤링 금지 우회 : "urllib.error.HTTPError: HTTP Error 403: Forbidden"
#opt.add_argument('User-Agent = "Mozilla/5.0"')

opt.add_experimental_option("excludeSwitches", ["enable-automation"])
opt.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome('c:/chromedriver/chromedriver.exe', options=opt)

driver.get('https://www.google.co.kr/imghp?hl=ko&ogbl')  # 구글 이미지 페이지
time.sleep(1) # 페이지 로딩시간

# 구글 검색란 선택 후 찾을 단어(키워드) 입력 & 엔터
elem = driver.find_element_by_name('q')  # class='gLFyf gsfi'
elem.send_keys(search_word)
elem.send_keys(Keys.RETURN)
time.sleep(1) # 페이지 전환시간

img_eles = driver.find_elements_by_css_selector("img[class='rg_i Q4LuWd']")
img_titles = driver.find_elements_by_css_selector("a[jsname='uy6ald']")
print("total images count : ", len(img_eles))

# %%
for i in range(len(img_eles)):
    try:
        img_eles[i].click()
        time.sleep(3)
        
        #img_final = driver.find_element_by_css_selector("img[class='n3VNCb")
        xpath = '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img'
        img_final = driver.find_element_by_xpath(xpath)
        bigImage_url = img_final.get_attribute("src")
        
        filename  = str(i+1)+ '_' + img_titles[i].get_attribute('title')
        filename = re.sub('[^가-힣A-Za-z0-9 _]+', '', filename)
        filename = filename.strip()
        if len(filename) >= 40:
                filename = filename[0:20]

        # 이미지 확장자가 있는 것과 없는 것을 구분하여 저장
        file_ext = bigImage_url.split('.')[-1]
        if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']: 
            filename = filename + '.' + file_ext              
        else:
            filename = filename + '.jpg'
        print(filename)
        
        request.urlretrieve(bigImage_url, att_folder + filename)
    except Exception as err:
        print(err)

# %%
