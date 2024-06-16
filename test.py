from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

XPATH_A = '/html/body/div[4]/table/tbody/tr/td[3]/div/div/table[2]/tbody/tr[2]/td[2]/ul/li[1]/button'

try:
    browser = webdriver.Chrome()
    browser.get('https://camping.gtdc.or.kr/DZ_reservation/reserCamping_v3.php?xch=reservation&xid=camping_reservation&sdate=202407')

    # 팝업 처리
    popup_xpath = "//input[@value='Y']"
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, popup_xpath))).click()

    # 팝업 제거
    popup2_xpath = "/html/body/div[1]/div/div[2]/button"
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, popup2_xpath))).click()

    # A구역 접속 버튼 클릭
    button = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, XPATH_A)))
    browser.execute_script("arguments[0].scrollIntoView(true);", button)
    button.click()
    print("A구역 접속 버튼 클릭 성공")

except Exception as e:
    print(f"A구역 접속 버튼 클릭 실패: {e}")

finally:
    time.sleep(500)
    browser.quit()




