from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib import request
import time
import os

def google_images(search_word):
    options = webdriver.ChromeOptions()
    options.add_argument('User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"')
    
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.google.co.kr/imghp?hl=ko&ogbl')
    time.sleep(1)
    
    # 구글 검색란 선택 후 찾을 단어(키워드) 입력
    elem = driver.find_element_by_name('q')  # class='gLFyf gsfi'
    elem.send_keys(search_word)
    elem.send_keys(Keys.RETURN)
    time.sleep(1)
    
    # 브라우저에서 스크롤 높이를 가져와서 변수에 저장
    # 'scrollHeight'는 스크롤 시키지 않았을때의 전체 높이
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    print(scroll_height)
    
    # 이미지 페이지 마지막까지 자동으로 스크롤하기
    while True:
        # 스크롤 높이(document.body.scrollHeight)까지 스크롤하기
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # 브라우저 로딩 시간
    
        # 스크롤 중단 지점에서 스크롤 위치(높이)를 파악하여 new_scroll_height에 저장하고,
        # 현재 스크롤 높이와 새로운 스크롤 높이가 같으면 끝까지 간 것이기 때문에 break 함
        new_scroll_height = driver.execute_script("return document.body.scrollHeight")
        
        if scroll_height == new_scroll_height:
            try:
                # 결과 더보기 버튼 처리 (버튼이 없을 경우 에러 발생하는 현상 예외 처리) - 2개 있음, xpath로 상세 처리함
                driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div[1]/div[2]/div[2]/input').click()  # input class='mye4qd'
            except:
                break
        scroll_height = new_scroll_height
    print('스크롤 완료')
   
    # 이미지 저장 폴더 생성
    try:
        if not os.path.exists(search_word):
            os.makedirs('C:/googleImage/' + search_word)
    except Exception as err:
        print(err)
        pass
    
    # 작은 이미지 전체 가져오기
    images = driver.find_elements_by_css_selector('img.rg_i.Q4LuWd')
    print(f'images count : {len(images)}')
    
    cnt = 0
    for image in images:
        # 이미지 다운로드 시 발생할 수 있는 오류 예외처리
        try:
            image.click()
            time.sleep(1)
            
            # 'img.n3VNCb'가 여러 개 있기 때문에 더 세부적으로 지정 필요
            xpath_= '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img'
            bigImage_url = driver.find_element_by_xpath(xpath_).get_attribute('src')
            file_ext = bigImage_url.split('.')[-1]
            
            # 이미지 확장자가 있는 것과 없는 것을 구분하여 저장
            if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                filename = str(time.time()) + '_' + os.path.basename(bigImage_url)  # 파일명만 추출
                    
                # 파일을 디렉토리에 저장
                request.urlretrieve(bigImage_url, 'D:/googleImage/' + search_word + '/' + filename)
                
                cnt += 1
                if cnt % 5 == 0:
                    print(f'검색어 "{search_word}"의 이미지 {cnt}장 저장 중...')            
            else:
                # print(bigImage_url)  # “data:image/jpeg;base64,/9j/4AAQSkZJR....”
                filename = str(time.time()) + '_.jpg'
                request.urlretrieve(bigImage_url, 'C:/googleImage/' + search_word + '/' + filename)
                cnt += 1
    
        except Exception as err:
            print(err)
        
        if cnt == 1:
            break
    
    print(f'검색어 "{search_word}"의 이미지 저장 완료!!')
        
    driver.close()

google_images('구름과 하늘')
 