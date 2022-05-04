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
    try:
        elements = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((kind, value))
        )
        return elements
    except:
        return None


# element 값 하나 반환
def getValue(driver: webdriver, timeout: int, kind: By, value: str) -> str:
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((kind, value))
        )
        return element.text
    except:
        return None


# iframe 전환
def switchToFrame(driver: webdriver, timeout: int, kind: By, value: str) -> bool:
    try:
        ack = WebDriverWait(driver, timeout).until(
            EC.frame_to_be_available_and_switch_to_it((kind, value))
        )
        return ack
    except: return False


# click 하기
def click(driver: webdriver, timeout: int, kind: By, value: str) -> bool:
    try:
        time.sleep(1)
        fetched = getElements(driver, timeout, kind, value)[0]
        time.sleep(1)
        fetched.click()
        return True
    except:
        print(traceback.format_exc())
        return False


# scroll 끝까지 내리기
def scrollDown(driver: webdriver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# 검색어 입력
def search(driver: webdriver, keyword: str) :
    search_path = XPath.searchPathKakao
    search_box = getElements(driver, 0.5, By.XPATH, search_path)
    actions = ActionChains(driver).send_keys_to_element(search_box[0], keyword).send_keys(Keys.ENTER)
    actions.perform()


# user hash값
def getUserHash(driver: webdriver) :
    buttonFollow = getElements(driver, 5, By.CLASS_NAME, '_2r43z')

    for i, j in enumerate(buttonFollow):
        userHashValue = buttonFollow[i].get_attribute('href').split('/')[-2]

    return userHashValue


# 도로명 주소 위도 경도 변환
def geocoding(geoLocal: Nominatim, address: str) -> (float, float):
    address = " ".join(address.split(' ')[:4])
    try :
        geo = geoLocal.geocode(address)
        return geo.latitude, geo.longitude
    except :
        return None, None


# json 파일 생성
def constructJson(fileName: str, data: list):
    with open(f'{fileName}.json', 'w', encoding='utf-8') as fp:
        json.dump(data, fp)


# pickle 파일 생성
def constructPickle(fileName: str, data):
    with open(f'{fileName}.pkl', 'wb') as f :
        pickle.dump(data, f)


# subway 맛집 검색
def getSuburl(driver: webdriver, sub):
    driver.get(URL.basePath)
    click(driver, timeout=1, value=XPath.sheild, kind=By.XPATH)
    time.sleep(1)
    search(driver, keyword=sub + "역 맛집")  # 검색어 입력
    click(driver, timeout=1, value=XPath.more, kind=By.XPATH)  ##  장소더보기 클릭 (모든 페이지 접근 위해)

# 모든 페이지 정보 불러오기
def getPageList(driver: webdriver, no):
    name_list = []
    time.sleep(1)
    click(driver, timeout=1, value=XPath.pageNo.format(no), kind=By.XPATH)  # 페이지 클릭
    time.sleep(1)
    name = getElements(driver, timeout=1, value=ClassName.place_kakao, kind=By.CLASS_NAME) # 페이지 내 모든 음식점 리스트 반환
    address = getElements(driver, timeout=1, value=ClassName.addr_kakao, kind=By.CLASS_NAME) # 페이지 내 모든 음식점 주소 반환
    for i in range(len(name)):
        if name[i].text not in name_list:
            name_list.append((name[i].text, " ".join(address[i].text.split()[:4])))
            print((name[i].text, " ".join(address[i].text.split()[:4])))
    return name_list



def getNamelist(driver: webdriver, sub_list):
    all_list = []
    try:
        for sub in sub_list:
            print(sub)
            getSuburl(driver, sub)
            for _ in range(7):
                for no in range(1, 6):
                    all_list += getPageList(driver, no)
                click(driver, timeout=5, value=XPath.nextPage, kind=By.XPATH)  # 다음페이지 클릭
        return all_list
    except:
        print(traceback.format_exc())
        return all_list

# place info dictionary 구조 반환
def placeInfoDict() -> dict:
    data = {
        'placeName': None,
        'placeType': None,
        'placeMeanRating': None,
        'placeAddress': None,
        'latitude': None,
        'longitude': None,
        'telephone': None,
        'description': None,
        'menu': dict(),
        'themeKeywords': [],
        'agePopularity': dict(),
        'genderPopularity': dict(),
        'time': dict(),
        'visitReviewNum': None,
        'blogReviewNum': None,
        'like': dict(),
    }
    return data