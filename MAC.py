from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 7.16 A구역
XPATH = '/html/body/div[4]/table/tbody/tr/td[3]/div/div/table[2]/tbody/tr[3]/td[3]/ul/li[1]/button'

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
    if click_button(XPATH):
        print("A구역 접속 버튼 클릭 성공")
    else:
        print("A구역 접속 버튼 클릭 실패")
        raise Exception("A구역 접속 버튼 클릭 실패")

    # 특정 위치 버튼 클릭 A134
    try:
        location_button_xpath = '//span[text()="A134"]/parent::button'
        job = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, location_button_xpath)))
        browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", job)
        time.sleep(1)
        browser.execute_script("arguments[0].click();", job)
        print("위치 버튼 클릭 성공")
    except Exception as e:
        print(f"위치 버튼 클릭 과정에서 오류 발생: {e}")

    # 인원(4명) 지정
    try:
        people_xpath = '/html/body/div[4]/table/tbody/tr/td[3]/div/div/table[1]/tbody/tr/td[4]/select/option[5]'
        browser.find_element(By.XPATH, people_xpath).click()
        print("인원 지정 성공")
    except Exception as e:
        print(f"인원 지정 과정에서 오류 발생: {e}")

    # 3박 4일
    try:
        stay_xpath = '/html/body/div[4]/table/tbody/tr/td[3]/div/div/div[5]/select/option[3]'
        browser.find_element(By.XPATH, stay_xpath).click()
        print("숙박 기간 지정 성공")
    except Exception as e:
        print(f"숙박 기간 지정 과정에서 오류 발생: {e}")

    print("무사히 지정 완료!")

except Exception as e:
    print(f"예약 과정에서 오류가 발생하였습니다: {e}")

finally:
    time.sleep(5000)
    browser.quit()  # 브라우저 종료