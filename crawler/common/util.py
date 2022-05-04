import pickle

from selenium import webdriver
import json
import pandas as pd
import re

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback

from geopy.geocoders import Nominatim
from config import *

# elements list 반환
from common.config import *


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
    except:
        return False


# click 하기
def click(driver: webdriver, timeout: int, kind: By, value: str) -> bool:
    try:
        fetched = getElements(driver, timeout, kind, value)[0]
        time.sleep(0.5)
        fetched.click()
        return True
    except:
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

# 리뷰 탭 클릭하기
def clickTab(driver: webdriver, name: str):
    tabElements = getElements(driver, 5, By.CLASS_NAME, ClassName.reviewTabClass)

    for i, j in enumerate(tabElements):
        if j.text == name:
            click(driver, 5, By.XPATH, XPath.reviewTab.format(index=i + 1))
            return i + 1

    return False

# 리뷰 최신 순으로 정렬하기 버튼
def clickRecent(driver: webdriver):
    # time.sleep(5)
    listButton = getElements(driver, 5, By.CLASS_NAME, ClassName.recentClass)

    if listButton != None:
        for i in listButton:
            if i.text == '최신순':
                i.click()


# url 정보에서 user hash value 가져오기
def getHashValue(driver: webdriver, timeout: int, kind: By, value1: str, value2: str) -> dict:
    userInfo = dict()
    try:
        # url-> hash value 추출
        element1 = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((kind, value1))
        )
        userInfo['userHash'] = element1.get_attribute('href').split('/')[-2]
        userInfo['리뷰'] = None
        userInfo['사진'] = None
        userInfo['팔로잉'] = None
        userInfo['팔로워'] = None
        # 포함된 user의 정보 가져오기
        element2 = getElements(element1, timeout, kind, value2)
        if element2 != None:
            for i in element2:
                info = i.text.split(' ')
                userInfo[info[0]] = info[1]

        return userInfo
    except:
        return None

def getReviewSubInfo(driver: webdriver, timeout: int, kind: By, value1: str, value2: str):
    reviewInfo = dict()
    reviewInfo['visitDay'] = None
    reviewInfo['visitCount'] = None
    reviewInfo['score'] = None
    try:
        element1 = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((kind, value1))
        )

        element2 = getElements(element1, timeout, kind, value2)

        if element2 != None:
            for i in element2:
                if '방문일' in i.text:
                    reviewInfo['visitDay'] = i.text.split('\n')[1]
                if '번째' in i.text:
                    reviewInfo['visitCount'] = i.text.split('\n')[0].strip('번째 방문')
                if '별점' in i.text:
                    reviewInfo['score'] = i.text.split('\n')[1]

        return reviewInfo
    except:
        return None


def getReviewInfo(driver: webdriver, placeName: str):
    print(placeName)
    print("OK")

    review = []  # element: list
    user = []  # element: dict
    userHash = set()  # user의 hashvalue 저장

    # search the place
    driver.get(URL.baseURL.format(placeName=placeName))

    # switch to the search iframe
    switchToFrame(driver, 5, By.XPATH, XPath.searchIframe)

    # click the first fetched item, 홈 화면으로 이동
    click(driver, 5, By.XPATH, XPath.firstFetched)

    # switch to the entry iframe
    driver.switch_to.parent_frame()
    if not switchToFrame(driver, 5, By.XPATH, XPath.entryIframe):
        print("There is no {} place".format(placeName))
        return None

    # click review tab
    clickTab(driver, '리뷰')

    # 최신순 버튼 클릭
    clickRecent(driver)

    # 리뷰 개수
    reviewCounts = getValue(driver, 5, By.CLASS_NAME, ClassName.reviewCountClass)
    reviewCount = int(re.sub(',', '', reviewCounts))
    print(reviewCount) #########이부분 sendData

    while True:
        if click(driver, 2, By.CLASS_NAME, ClassName.reviewMoreButtonClass) == False:
            break

    # 현재 페이지 리뷰 element들 가져오기
    reviewElements = driver.find_elements(by=By.CLASS_NAME, value=ClassName.reviewClass)

    if reviewElements != None:

        # 각 리뷰에서 정보 가져오기
        for i in range(len(reviewElements)):

            click(reviewElements[i], 1, By.CLASS_NAME, ClassName.reviewMorePointButtonClass)
            click(reviewElements[i], 1, By.CLASS_NAME, ClassName.reviewMoreContentButtonClass)

            # 리뷰 유저의 ID -> str
            reviewUserId = getValue(reviewElements[i], 1, By.CLASS_NAME, ClassName.reviewUserId)

            if reviewUserId == None:
                continue

            # 리뷰 유저에 대한 정보 -> dict
            reviewUserHash = getHashValue(reviewElements[i], 1, By.CLASS_NAME, ClassName.reviewUserHash1,
                                          ClassName.reviewUserHash2)
            # 리뷰 내용 -> str
            reviewContent = getValue(reviewElements[i], 1, By.CLASS_NAME, ClassName.reviewContent)

            # review 별점, 방문날짜, 방문 횟수 - dict
            reviewInfo = getReviewSubInfo(reviewElements[i], 1, By.CLASS_NAME, ClassName.reviewInfo1,
                                       ClassName.reviewInfo2)

            if reviewInfo != None:
                if len(reviewInfo['visitDay'].split('.')) != 3:
                    break

            if reviewUserHash == None:
                continue

            if reviewUserHash['userHash'] not in userHash:
                reviewUserHash['userId'] = reviewUserId
                userHash.add(reviewUserHash['userHash'])
                user.append(reviewUserHash)

                print(reviewUserHash['userHash']) #########이부분 sendData -> 유니크 유저 해시값
                print(reviewUserHash) #########이부분 sendData -> 리뷰 마다 유저 정보 send

            # 0. 유저 해시값
            # 1. 아이디
            # 2. 내용
            # 3. 평점
            # 4. 날짜
            # 5. 방문횟수

            result = [
                reviewUserHash['userHash'], reviewUserId, reviewContent, reviewInfo['score'], reviewInfo['visitDay'],
                reviewInfo['visitCount']
            ]

            review.append(result)
            print(result) #########이부분 sendData
