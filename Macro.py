from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# WebDriver 초기화
#xpath 반드시 확인하자.
# 7.15 A구역
XPATH = '/html/body/div[4]/table/tbody/tr/td[3]/div/div/table[2]/tbody/tr[2]/td[2]/ul/li[1]/button'

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

try:
    browser = webdriver.Chrome()
    url = 'https://camping.gtdc.or.kr/DZ_reservation/reserCamping_v3.php?xch=reservation&xid=camping_reservation&sdate=202407'
    browser.get(url)

    clock("10:00") #함수 적용

    # 팝업 처리
    popup_xpath = "//input[@value='Y']"
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, popup_xpath)))
    browser.execute_script("arguments[0].click();", browser.find_element(By.XPATH, popup_xpath))

    # 팝업 제거
    popup2_xpath = "/html/body/div[1]/div/div[2]/button"
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, popup2_xpath)))
    browser.execute_script("arguments[0].click();", browser.find_element(By.XPATH, popup2_xpath))

    # 날짜 선택
    date_xpath = "//button[@value='C:2024-07-15']"
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, date_xpath)))
    print("날짜 선택 완료")

    # A구역 접속 버튼 클릭
    button = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, XPATH)))
    browser.execute_script("arguments[0].scrollIntoView(true);", button)
    button.click()
    print("A구역 접속 버튼 클릭 성공")

    def click_button():
        try:
            button = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, XPATH)))
            browser.execute_script("arguments[0].scrollIntoView(true);", button)
            browser.execute_script("arguments[0].click();", button)
            print(f"버튼 클릭 성공: {XPATH}")
            return True
        except Exception as e:
            print(f"버튼 클릭 실패: {e}")
            return False

    # 특정 위치 버튼 클릭
    location_button_xpath = '/html/body/div[4]/table/tbody/tr/td[3]/div/div/div[4]/div/button[49]'
    if click_button(location_button_xpath):
        print("특정 위치 버튼 클릭 성공")
    else:
        print("특정 위치 버튼 클릭 실패")

except Exception as e:
    print(f"예약 과정에서 오류가 발생하였습니다: {e}")

finally:
    time.sleep(500)
    browser.quit()  # 브라우저 종료
