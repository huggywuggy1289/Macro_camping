from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# WebDriver 초기화
browser = webdriver.Chrome()
browser.maximize_window()  # 브라우저 창 최대화

XPATH = [
    #7.14 A구역
    '/html/body/div[4]/table/tbody/tr/td[3]/div/div/table[2]/tbody/tr[3]/td[1]/ul/li[1]/button'
]
# 예약 버튼 클릭
def click_button(xpath):
    try:
        button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        browser.execute_script("arguments[0].scrollIntoView(true);", button)
        browser.execute_script("arguments[0].click();", button)
        print(f"버튼 클릭 성공: {xpath}")
        return True
    except Exception as e:
        print(f"버튼 클릭 실패: {e}")
        return False
#---------------------------------------------------------------
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

    # A구역 접속 버튼 클릭 시도
    if not click_button(XPATH[0]):
        raise Exception("A구역 접속 버튼 클릭 실패")

    # 특정 위치 버튼 클릭 (A147 예시)
    location_button_xpath = '/html/body/div[4]/table/tbody/tr/td[3]/div/div/div[4]/div/button[47]'
    if click_button(location_button_xpath):
        print("특정 위치 버튼 클릭 성공")
    else:
        print("특정 위치 버튼 클릭 실패")

except Exception as e:
    print(f"예약 과정에서 오류가 발생하였습니다: {e}")

finally:
    time.sleep(10)
    browser.quit()  # 브라우저 종료



# 1명 : /html/body/div[4]/table/tbody/tr/td[3]/div/div/table[1]/tbody/tr/td[4]/select/option[2]
# 2명 : /html/body/div[4]/table/tbody/tr/td[3]/div/div/table[1]/tbody/tr/td[4]/select/option[3]
# 3명 : /html/body/div[4]/table/tbody/tr/td[3]/div/div/table[1]/tbody/tr/td[4]/select/option[4]
# 4명 : /html/body/div[4]/table/tbody/tr/td[3]/div/div/table[1]/tbody/tr/td[4]/select/option[5]
# 5명 : /html/body/div[4]/table/tbody/tr/td[3]/div/div/table[1]/tbody/tr/td[4]/select/option[6]


#----------------------------------------------------------------------------------------
    # def click_random_button(elements):
    #     try:
    #         elements = browser.find_elements(By.CLASS_NAME, 'areacode')
    #         print(f"총 {len(elements)}개의 버튼 요소 찾음")

    #         while elements:
    #             random_button = random.choice(elements)
    #             random_button.click()
    #             print("무작위 버튼 클릭 완료")
    #             return True

    #     except (NoSuchElementException, ElementClickInterceptedException) as e:
    #             print(f"버튼 클릭 실패: {e}")

    #     print("예약 가능한 버튼을 더 이상 찾을 수 없습니다.")
    #     return False
    
    
    # while click_random_button():
    #     # 인원 지정 (예: 4명)
    #     people_xpath = '/html/body/div[4]/table/tbody/tr/td[3]/div/div/table[1]/tbody/tr/td[4]/select/option[5]'  # 4명 예시
    #     WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, people_xpath))).click()
    #     print("인원 지정 완료")

    #     # 예약 기간 설정 (3박 4일)
    #     duration_xpath = '//html/body/div[4]/table/tbody/tr/td[3]/div/div/div[5]/select/option[3]'  # 3박 4일 선택
    #     WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, duration_xpath))).click()
    #     print("예약 기간 설정 완료")
#-----------------------------------------------------------------------------------------