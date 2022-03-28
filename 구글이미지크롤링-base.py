from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib import request
import time

driver = webdriver.Chrome()
driver.get('https://www.google.co.kr/imghp?hl=ko&ogbl')  # 구글 이미지 페이지
time.sleep(1) # 페이지 로딩시간

elem = driver.find_element_by_name('q')  # class='gLFyf gsfi'
elem.send_keys('파란하늘')
elem.send_keys(Keys.RETURN)
time.sleep(1) # 페이지 전환시간

# 검색 결과, 이미지 페이지 상에서 클릭 시 큰 이미지 보기와 큰 이미지의 링크 주소 확인 
driver.find_elements_by_css_selector('img.rg_i.Q4LuWd')[0].click()
# <img class="rg_i Q4LuWd"> --> .rg_i.Q4LuWd or img.rg_i.Q4LuWd
time.sleep(1)  # 이미지 로딩 시간 주기

# 작은 이미지를 클릭한 페이지에서 큰 이미지를 선택 <img class='n3VNCb'>
big_image = driver.find_element_by_css_selector('img.n3VNCb')  
print(big_image)
# <selenium.webdriver.remote.webelement.WebElement 
# (session="c60d552e6ead7566bb625638934dec9f", element="a1ecafb7-acbe-4c87-83a7-8b7c586e3096")>

# 이미지 src 속성(URL)가져오기
bigImage_url = big_image.get_attribute('src')  
print(bigImage_url)
# http://ojsfile.ohmynews.com/STD_IMG_FILE/2018/0103/IE002266925_STD.jpg

# 이미지 다운로드
request.urlretrieve(bigImage_url, "image01.jpg")

driver.close()