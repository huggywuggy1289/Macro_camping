from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import cv2
import numpy as np
import pytesseract
# from pytesseract import image_to_string
from PIL import Image
from captcha.image import ImageCaptcha

# 자동방지입력문자
pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\손재윤\\OneDrive\\바탕 화면\\tesseract-5.4.1\\tesseract.exe"

# A구역
XPATH = '/html/body/div[4]/table/tbody/tr/td[3]/div/div/table[2]/tbody/tr[3]/td[4]/ul/li[1]/button'

def clock(target_time):
    while True:
        current_time = datetime.now().strftime("%H:%M") # 시:분]
        if target_time == current_time or target_time < current_time:
            print(f"현재 시간: {current_time} - 예약을 시도합니다!")
            break
        else:
            print(f"현재 시간: {current_time} - 기다리는 중...")
            time.sleep(5)  # 5초 대기 후 다시 체크
            browser.refresh()

def click_button(xpath):
    try:
        button = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        time.sleep(1)
        browser.execute_script("arguments[0].click();", button)
        print(f"버튼 클릭 성공: {xpath}")
        return True
    except Exception as e:
        print(f"버튼 클릭 실패: {e}")
        return False

try:
    browser = webdriver.Chrome()
    url = 'https://camping.gtdc.or.kr/DZ_reservation/reserCamping_v3.php?xch=reservation&xid=camping_reservation&sdate=202407'
    browser.get(url)

    # 팝업 처리
    popup_xpath = "//input[@value='Y']"
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, popup_xpath)))
    browser.execute_script("arguments[0].click();", browser.find_element(By.XPATH, popup_xpath))

    # 팝업 제거
    popup2_xpath = "/html/body/div[1]/div/div[2]/button"
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, popup2_xpath)))
    browser.execute_script("arguments[0].click();", browser.find_element(By.XPATH, popup2_xpath))

    clock("10:00") #함수 적용

    # 날짜 선택
    date_xpath = "//button[@value='C:2024-07-17']"
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, date_xpath)))
    print("날짜 선택 완료")

    # A구역 접속 버튼 클릭
    if click_button(XPATH):
        print("A구역 접속 버튼 클릭 성공")
    else:
        print("A구역 접속 버튼 클릭 실패")
        raise Exception("A구역 접속 버튼 클릭 실패")

    # 특정 위치 버튼 클릭
    try:
        location_button_xpath = ['//span[text()="A147"]/parent::button',
                                 '//span[text()="A149"]/parent::button',
                                 '//span[text()="A129"]/parent::button',
                                 '//span[text()="A128]/parent::button']
        for path in location_button_xpath:
            try:
                job = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, path)))
                browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", job)
                browser.execute_script("arguments[0].click();", job)
                print(f"위치 버튼 클릭 성공: {path}")

                people_xpath = '/html/body/div[4]/table/tbody/tr/td[3]/div/div/table[1]/tbody/tr/td[4]/select/option[5]'
                browser.find_element(By.XPATH, people_xpath).click()
                print("인원 지정 성공")

            except Exception as e:
                print(f"위치 버튼 클릭 실패: {path} - {e}")
                continue

    except Exception as e:
        print(f"위치 버튼 클릭 과정에서 오류 발생: {e}")

    # 3박 4일
    try:
        stay_xpath = '/html/body/div[4]/table/tbody/tr/td[3]/div/div/div[5]/select/option[3]'
        browser.find_element(By.XPATH, stay_xpath).click()
        print("숙박 기간 지정 성공")
    except Exception as e:
        print(f"숙박 기간 지정 과정에서 오류 발생: {e}")

    print("무사히 지정 완료!")

    try:
        # 캡차 이미지 찾기 및 저장
        captcha_image = browser.find_element(By.XPATH, '/html/body/div[4]/table/tbody/tr/td[3]/div/div/table[3]/tbody/tr/td/img')
        captcha_image.screenshot('captcha.png')

        def get_macro_protection_number(img):
            image_grey = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
            max_output_value = 255
            neighborhood_size = 99
            subtract_from_mean = 10
            image_binarized = cv2.adaptiveThreshold(image_grey,
                                                max_output_value,
                                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                cv2.THRESH_BINARY + cv2.THRESH_OTSU,
                                                neighborhood_size,
                                                subtract_from_mean)                                    
            result = pytesseract.image_to_string(image_binarized, config='--psm 6 -c tessedit_char_whitelist=0123456789')
            print("분석결과 :",result)
            return result
        
        # OCR추가: 단일문자 인식 --psm 6 (참고: https://m.blog.naver.com/johnsmithbrainseven/222242853850)
        # OCR 적용
        captcha_text = get_macro_protection_number('captcha.png')
        print(f'Extracted CAPTCHA text: {captcha_text}')

        # 텍스트 입력
        # OCR추가: 단일문자 인식 --psm 6 (참고: https://m.blog.naver.com/johnsmithbrainseven/222242853850)
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
        captcha_text = pytesseract.image_to_string(Image.open('captcha.png'), config=custom_config)
        print(captcha_text)

        # 제출 버튼 클릭
        xpath_next = "/html/body/div[4]/table/tbody/tr/td[3]/div/div/div[6]/button[2]" 
        browser.find_element(By.XPATH, xpath_next).click()
        print("자동방지문자 우회성공")

    except Exception as e:
        print("방지문자 입력과정에서 오류발생!")

except Exception as e:
    print(f"예약 과정에서 오류가 발생하였습니다: {e}")

finally:
    time.sleep(5000)




