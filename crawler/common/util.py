from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from config import URL, Selector, XPath, ClassName
import time

# elements list 반환
def getElements(driver: webdriver, timeout: int, kind: By, value: str) -> list:
    elements = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((kind, value))
    )
    return elements


# iframe 전환
def switchToFrame(driver: webdriver, timeout: int, kind: By, value: str) -> bool:
    ack = WebDriverWait(driver, timeout).until(
        EC.frame_to_be_available_and_switch_to_it((kind, value))
    )
    return ack

# click 하기
def click(driver: webdriver, timeout: int, kind: By, value: str) -> bool:
    try :
        fetched = getElements(driver, timeout, kind, value)
        time.sleep(0.5)
        fetched.click()
        return True
    except :
        return False

# scroll 끝까지 내리기
def scrollDown(driver: webdriver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# 검색어 입력
def search(driver: webdriver, keyword: str) :
    search_path = Selector.search_path_kakao
    search_box = getElements(driver, By.XPATH, search_path)
    actions = ActionChains(driver).send_keys_to_element(search_box, keyword).send_keys(Keys.ENTER)
    actions.perform()

# user hash값
def getUserHash(driver: webdriver) :
    buttonFollow = getElements(driver, 5, By.CLASS_NAME, '_2r43z')

    for i, j in enumerate(buttonFollow):
        userHashValue = buttonFollow[i].get_attribute('href').split('/')[-2]

    return userHashValue
