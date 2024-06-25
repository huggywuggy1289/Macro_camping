from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options
import cv2
import numpy as np
import pytesseract
from pytesseract import image_to_string
from PIL import Image
from captcha.image import ImageCaptcha

# 자동방지입력문자(텍스트 이미지를 추출하는데 사용)
pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\손재윤\\OneDrive\\바탕 화면\\tesseract-5.4.1\\tesseract.exe"

# A구역(수정요망/날짜별로 tr과 td가 다름)
XPATH = '/html/body/div[4]/table/tbody/tr/td[3]/div/div/table[2]/tbody/tr[3]/td[4]/ul/li[1]/button'
# '/html/body/div[4]/table/tbody/tr/td[3]/div/div/table[2]/tbody/tr[4]/td[4]/ul/li[1]/button'

def clock(target_time):
    while True:
        current_time = datetime.now().strftime("%H:%M") # 시:분
        if target_time == current_time or target_time < current_time:
            print(f"현재 시간: {current_time} - 예약을 시도합니다!")
            break
        else:
            print(f"현재 시간: {current_time} - 기다리는 중...")
            time.sleep(1)  # 5초 대기 후 다시 체크
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
    chrome_options = webdriver.ChromeOptions()

    browser = webdriver.Chrome()
    chrome_options.add_argument("--headless")  # 헤드리스 모드 사용
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
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

    # 날짜 선택(수정요망)
    date_xpath = "//button[@value='C:2024-07-17']"
    WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, date_xpath)))
    print("날짜 선택 완료")

    # A구역 접속 버튼 클릭
    if click_button(XPATH):
        print("A구역 접속 버튼 클릭 성공")

        # 특정 위치 버튼 클릭
        location_button_xpath = ['/html/body/div[4]/table/tbody/tr/td[3]/div/div/div[4]/div/button[47]',
                                 '/html/body/div[4]/table/tbody/tr/td[3]/div/div/div[4]/div/button[49]',
                                 '/html/body/div[4]/table/tbody/tr/td[3]/div/div/div[4]/div/button[36]',
                                 '/html/body/div[4]/table/tbody/tr/td[3]/div/div/div[4]/div/button[31]',
                                 '/html/body/div[4]/table/tbody/tr/td[3]/div/div/div[4]/div/button[53]',
                                 '/html/body/div[4]/table/tbody/tr/td[3]/div/div/div[4]/div/button[29]',
                                 '/html/body/div[4]/table/tbody/tr/td[3]/div/div/div[4]/div/button[21]']
        
        for path in location_button_xpath:
            try:
                try:
                    job = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, path)))
                    browser.execute_script("arguments[0].click();", job)
                    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", job)
                    print(f"위치 버튼 클릭 성공: {path}")
                except Exception as e:
                    print("A구역 접속 실패")

                try:
                    people_xpath = '/html/body/div[4]/table/tbody/tr/td[3]/div/div/table[1]/tbody/tr/td[4]/select/option[5]'
                    browser.find_element(By.XPATH, people_xpath).click()
                    print("인원 지정 성공")

                except Exception as e:
                    print(f"인원 지정 실패: {path} - {e}")
                
                try:
                    # 숙박 기간 선택 : '/html/body/div[4]/table/tbody/tr/td[3]/div/div/div[5]/select/option[3]'
                    stay_xpath = ['/html/body/div[4]/table/tbody/tr/td[3]/div/div/div[5]/select/option[2]']
                    for stay in stay_xpath:
                        stay_element = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, stay)))
                        stay_element.click()
                        break
                    print("숙박 기간 지정 성공!")
                    break  # 인원 지정과 숙박 기간 지정이 성공하면 루프를 빠져나감
                except Exception as e:
                    print(f"숙박 기간 지정 실패: {path} - {e}")

            except Exception as e:
                print(f"위치 버튼 클릭 실패: {path} - {e}")
                continue
    else:
        print("접속 실패")
        raise Exception("접속 실패")

    try:
        # 캡차 이미지 찾기 및 저장
        captcha_image = browser.find_element(By.XPATH, '/html/body/div[4]/table/tbody/tr/td[3]/div/div/table[3]/tbody/tr/td/img')
        captcha_image.screenshot('captcha.png')

        # OCR추가: 단일문자 인식 --psm 6 (참고: https://m.blog.naver.com/johnsmithbrainseven/222242853850)
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
        captcha_text = pytesseract.image_to_string(Image.open('captcha.png'), config=custom_config)
        print(captcha_text)

        # 텍스트 입력
        captcha_input = browser.find_element(By.XPATH, '/html/body/div[4]/table/tbody/tr/td[3]/div/div/table[3]/tbody/tr/td/input')
        browser.execute_script("arguments[0].value = arguments[1];", captcha_input, captcha_text)
        print(f'입력된 캡챠 텍스트: {captcha_input.get_attribute("value")}')

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
    # browser.quit()  # 브라우저 종료


    # 1박 2일 : /html/body/div[4]/table/tbody/tr/td[3]/div/div/div[5]/select/option[1]
    # 2박 3일 : /html/body/div[4]/table/tbody/tr/td[3]/div/div/div[5]/select/option[2]
    # 3박 4일 : /html/body/div[4]/table/tbody/tr/td[3]/div/div/div[5]/select/option[3]