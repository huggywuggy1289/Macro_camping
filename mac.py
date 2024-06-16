import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

# WebDriver 초기화
browser = webdriver.Chrome()
browser.maximize_window()  # 브라우저 창 최대화
browser.get('https://www.google.co.kr/')

XPATH = [
    #7.14 A구역
    '/html/body/div[4]/table/tbody/tr/td[3]/div/div/table[2]/tbody/tr[3]/td[1]/ul/li[1]/button'
]

try:
    url = 'https://camping.gtdc.or.kr/DZ_reservation/reserCamping_v3.php?xch=reservation&xid=camping_reservation&sdate=202407&step=Areas'
    browser.get(url)

    # 팝업 처리
    popup_xpath = "//input[@value='Y']"
    browser.find_element(By.XPATH, popup_xpath).click()
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, popup_xpath))).click()

    # 팝업 제거
    popup2_xpath = "/html/body/div[1]/div/div[2]/button"
    browser.find_element(By.XPATH, popup2_xpath).click()
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, popup2_xpath))).click()

    # 날짜 선택
    date_xpath = "//button[@value='C:2024-07-14']"
    browser.find_element(By.XPATH, date_xpath).click()
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, date_xpath))).click()
    print("날짜 선택 완료")

    # 예약 버튼 클릭
    def click_reservation_button():
        for path in XPATH:
            try:
                reservation_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, path)))
                reservation_button.click()
                print(f"7월 14일 예약 버튼 클릭 성공: {path}")
                return True
            except Exception as e:
                print(f"예약 버튼 클릭 실패: {e}")
                continue
        return False

    # 예약 버튼 클릭 시도
    while not click_reservation_button():
        time.sleep(0.1)  # 짧은 시간 대기 후 다시 시도
    print("예약 절차를 마무리했으니 다음단계로 진행하세요.")

    # 위치 선정 버튼 클릭
    location_buttons = [
        '/html/body/div[4]/table/tbody/tr/td[3]/div/div/div[4]/div/button[47]'  # A147
    ]

    for btn_xpath in location_buttons:
        try:
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, btn_xpath))).click()
            browser.execute_script("arguments[0].click();", browser.find_element(By.XPATH, btn_xpath))
            print(f"위치 선정 버튼 클릭 성공: {btn_xpath}")
            break  # 성공적으로 클릭했으면 반복 종료
        except Exception as e:
            print(f"위치 선정 버튼 클릭 실패: {e}")
            continue

    # 인원 지정
    people_xpath = '/html/body/div[4]/table/tbody/tr/td[3]/div/div/table[1]/tbody/tr/td[4]/select/option[5]'  # 4명 예시
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, people_xpath))).click()
    browser.execute_script("arguments[0].click();", browser.find_element(By.XPATH, people_xpath))
    print("인원 지정 완료")

    # 예약 기간 설정
    duration_xpath = '/html/body/div[4]/table/tbody/tr/td[3]/div/div/div[5]/select/option[3]'  # 3박 4일 선택
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, duration_xpath))).click()
    browser.execute_script("arguments[0].click();", browser.find_element(By.XPATH, duration_xpath))
    print("예약 기간 설정 완료")

except Exception as e:
    print(f"예약 과정에서 오류가 발생하였습니다: {e}")

finally:
    time.sleep(10)

# 1명 : /html/body/div[4]/table/tbody/tr/td[3]/div/div/table[1]/tbody/tr/td[4]/select/option[2]
# 2명 : /html/body/div[4]/table/tbody/tr/td[3]/div/div/table[1]/tbody/tr/td[4]/select/option[3]
# 3명 : /html/body/div[4]/table/tbody/tr/td[3]/div/div/table[1]/tbody/tr/td[4]/select/option[4]
# 4명 : /html/body/div[4]/table/tbody/tr/td[3]/div/div/table[1]/tbody/tr/td[4]/select/option[5]
# 5명 : /html/body/div[4]/table/tbody/tr/td[3]/div/div/table[1]/tbody/tr/td[4]/select/option[6]
