from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from geopy.geocoders import Nominatim
import time
import json
import pickle
import traceback

from common.config import URL, Selector, XPath, ClassName


# elements list 반환
def getElements(driver: webdriver, timeout: int, kind: By, value: str) -> list:
    try :
        elements = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((kind, value))
        )
        return elements
    except :
        return None


# element 값 하나 반환
def getValue(driver: webdriver, timeout: int, kind: By, value: str) -> str:
    try :
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((kind, value))
        )
        return element.text
    except :
        return None


# iframe 전환
def switchToFrame(driver: webdriver, timeout: int, kind: By, value: str) -> bool:
    try :
        ack = WebDriverWait(driver, timeout).until(
            EC.frame_to_be_available_and_switch_to_it((kind, value))
        )
        return ack
    except : return False


# click 하기
def click(driver: webdriver, timeout: int, kind: By, value: str) -> bool:
    try :
        fetched = getElements(driver, timeout, kind, value)[0]
        time.sleep(0.5)
        fetched.click()
        return True
    except :
        return False


# scroll 끝까지 내리기
def scrollDown(driver: webdriver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# 검색어 입력
def search(driver: webdriver, keyword: str):
    search_path = Selector.search_path_kakao
    search_box = getElements(driver, By.XPATH, search_path)
    actions = ActionChains(driver).send_keys_to_element(search_box, keyword).send_keys(Keys.ENTER)
    actions.perform()


# user hash값
def getUserHash(driver: webdriver):
    buttonFollow = getElements(driver, 5, By.CLASS_NAME, '_2r43z')

    for i, j in enumerate(buttonFollow):
        userHashValue = buttonFollow[i].get_attribute('href').split('/')[-2]

    return userHashValue


# 도로명 주소 위도 경도 변환
def geocoding(geoLocal: Nominatim, address: str) -> (float, float):
    address = " ".join(address.split(' ')[:4])
    try:
        geo = geoLocal.geocode(address)
        return geo.latitude, geo.longitude
    except:
        return None, None


# json 파일 생성
def constructJson(fileName: str, data: list):
    with open(f'{fileName}.json', 'w', encoding='utf-8') as fp:
        json.dump(data, fp)


# pickle 파일 생성
def constructPickle(fileName: str, data):
    with open(f'{fileName}.pkl', 'wb') as f:
        pickle.dump(data, f)
