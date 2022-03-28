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

ssl._create_default_https_context = ssl._create_unverified_context

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('에러 : 폴더 만들기 실패 ' +  directory)
        sys.exit()

today = str(datetime.datetime.today())[0:16].replace("-", "").replace(" ", "_").replace(":", "")
   
att_base = './구글이미지(첨부파일)'
att_folder = f'{att_base}/{today}/'

createFolder(att_base)
createFolder(att_folder)


opt = Options()
opt.add_argument('--start-maximized')
opt.add_argument('User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"')
opt.add_experimental_option("excludeSwitches", ["enable-automation"])
opt.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome('c:/chromedriver/chromedriver.exe', options=opt)

driver.get('https://www.google.co.kr/imghp?hl=ko&ogbl')  # 구글 이미지 페이지
time.sleep(1) # 페이지 로딩시간

# 구글 검색란 선택 후 찾을 단어(키워드) 입력 & 엔터
elem = driver.find_element_by_name('q')  # class='gLFyf gsfi'
elem.send_keys('pokemon')
elem.send_keys(Keys.RETURN)
time.sleep(1) # 페이지 전환시간

img_eles = driver.find_elements_by_css_selector("img[class='rg_i Q4LuWd']")
print(len(img_eles))


# %%
cnt = 0

for i in range(len(img_eles)):
    print(i, "clicking")

    img_eles[i].click()
    print(i, "clicked!!!")
    time.sleep(3)

    #img_final = driver.find_element_by_css_selector("img[class='n3VNCb")
    xpath = '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img'
    img_final = driver.find_element_by_xpath(xpath)
    bigImage_url = img_final.get_attribute("src")
    #time.sleep(1)

    file_ext = bigImage_url.split('.')[-1]

    # 이미지 확장자가 있는 것과 없는 것을 구분하여 저장
    if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
        print(i, bigImage_url)
        
        #filename = str(time.time()) + '_' + os.path.basename(bigImage_url)  # 파일명만 추출
        filename = str(i)+ '_' + img_eles[i].get_attribute('alt')
        filename = re.sub('[^A-Za-z0-9 _]+', '', filename)
        if len(filename) >= 20:
            filename = filename[0:20]
        filename = filename + '.' + file_ext
        #filename = filename.replace("|", "_").replace("&", "_").replace("?", "_")
        request.urlretrieve(bigImage_url, att_folder + filename)
        
        if i % 5 == 0:
            print(f'검색어 이미지 {cnt}장 저장 중...')  
                  
    else:
        print(i)
        
        # print(bigImage_url)  # “data:image/jpeg;base64,/9j/4AAQSkZJR....”
        # filename = str(i) + '_' + str(time.time()) + '_.jpg'
        filename = img_eles[i].get_attribute('alt')
        filename = re.sub('[^A-Za-z0-9 _]+', '', filename)
        if len(filename) >= 20:
            filename = filename[0:20]
        filename = str(i)+ '_' + filename + '.jpg'
        
        
        #filename = filename.replace("|", "_").replace("&", "_").replace("?", "_")
        print(filename)
        
        request.urlretrieve(bigImage_url, att_folder + filename)


# %%
