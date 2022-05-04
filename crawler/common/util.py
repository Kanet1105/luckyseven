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
from config import Selector

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

    except:
        return False


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

def getPlaceInfoDetails(driver: webdriver, geoLocal: Nominatim, name: str):
    data = placeInfoDict()

    # search the place
    driver.get(URL.baseURL.format(placeName=name))

    # switch to the search iframe
    switchToFrame(driver, 5, By.XPATH, XPath.searchIframe)
    # click the first fetched item
    click(driver, 5, By.XPATH, XPath.firstFetched)

    # switch to the entery iframe
    driver.switch_to.parent_frame()
    if not switchToFrame(driver, 5, By.XPATH, XPath.entryIframe):
        print("No place : ", name)
        return None

    click(driver, 5, By.XPATH, XPath.homePath)
    # get place name, place type
    data['placeName'] = getElements(driver, 5, By.XPATH, XPath.placeName)[0].text
    data['placeType'] = getElements(driver, 5, By.XPATH, XPath.placeType)[0].text

    # get place mean rating
    num = 1
    placeMeanRating = getValue(driver, 5, By.XPATH, XPath.placeMeanRating)
    if placeMeanRating:
        data['placeMeanRating'] = float(placeMeanRating)
        num += 1
    # get number of reviews
    visitReviewNum = getValue(driver, 5, By.XPATH, XPath.reviewNum.format(num=num))
    if visitReviewNum:
        data['visitReviewNum'] = int(visitReviewNum.replace(',', ''))
        num += 1
    blogReviewNum = getValue(driver, 5, By.XPATH, XPath.reviewNum.format(num=num))
    if blogReviewNum:
        data['blogReviewNum'] = int(blogReviewNum.replace(',', ''))

    # get telephone
    data['telephone'] = getValue(driver, 5, By.CLASS_NAME, ClassName.telephoneClass)

    # get address
    placeAddress = getValue(driver, 5, By.CLASS_NAME, ClassName.placeAddressClass)
    if placeAddress:
        data['placeAddress'] = placeAddress
        latitude, longitude = geocoding(geoLocal, placeAddress)
        data['latitude'], data['longitude'] = latitude, longitude

    divNum = 1
    if getElements(driver, 5, By.CLASS_NAME, ClassName.zeroClass):
        divNum += 1
    if getElements(driver, 5, By.CLASS_NAME, ClassName.announcementClass):
        divNum += 1

    informationList = getElements(driver, 5, By.CSS_SELECTOR, Selector.informationSelector.format(num=5))
    for index, information in enumerate(informationList, start=1):
        infoText = information.text.split('\n')
        if infoText[0] == '영업시간':
            # more buttom click
            if not click(driver, 5, By.XPATH, XPath.timeMoreButton.format(divNum=divNum, idx=index)):
                if not click(driver, 5, By.XPATH, XPath.timeMoreButton2.format(divNum=divNum, idx=index)):
                    click(driver, 5, By.XPATH, XPath.timeMoreButton3.format(divNum=divNum, idx=index))

            dayList = getElements(driver, 5, By.CLASS_NAME, ClassName.dayClass)
            timeList = getElements(driver, 5, By.CLASS_NAME, ClassName.timeClass)
            if not dayList or not timeList:
                continue
            for idx in range(len(dayList)):
                data['time'][dayList[idx].text] = timeList[1:][idx].text
        elif infoText[0] == '설명':
            if not click(driver, 5, By.XPATH, XPath.descriptionMoreButton.format(divNum=divNum, idx=index)):
                click(driver, 5, By.XPATH, XPath.descriptionMoreButton2.format(divNum=divNum, idx=index))
            description = getElements(driver, 5, By.XPATH,
                                      XPath.description.format(divNum1=5, divNum2=divNum, idx=index))
            if not description:
                description = getElements(driver, 5, By.XPATH,
                                          XPath.description.format(divNum1=6, divNum2=divNum, idx=index))
            if description:
                data['description'] = ' '.join(description[-1].text.split('내용 더보기')[0].split('\n'))

    scrollDown(driver)
    # get theme keyword
    if getElements(driver, 5, By.CLASS_NAME, ClassName.themeKeywordClass):
        themeData = getElements(driver, 5, By.CLASS_NAME, ClassName.themeDataClass)
        for value in themeData:
            data['themeKeywords'].append(value.text.split(', ')[-1])
    # get popularity
    tabList = getElements(driver, 5, By.XPATH, XPath.placeTab)
    if tabList:
        tabList = tabList[0].text.replace('\n', ' ').split(' ')
        if '메뉴' in tabList:
            divNum += 2
        else:
            divNum += 1
    else:
        tabList = []

    click(driver, 5, By.XPATH, XPath.datalabMoreButton.format(divNum=divNum))
    if getElements(driver, 5, By.CLASS_NAME, ClassName.popularityClass):
        for idx in range(10, 70, 10):
            data['agePopularity'][f'{idx}대'] = float(
                getValue(driver, 5, By.XPATH, XPath.agePopluarity.format(age=idx // 10)).replace('%', ''))
        genderData = getElements(driver, 5, By.CLASS_NAME, ClassName.donutGraphClass)[0]
        if genderData:
            genderPopularity = genderData.text.split('\n')
            data['genderPopularity']['F'] = int(genderPopularity[0].split('%')[0])
            data['genderPopularity']['M'] = int(genderPopularity[1].split('%')[0])

    for idx, tab in enumerate(tabList, start=1):
        if tab == '메뉴' and not data['menu']:
            if not click(driver, 5, By.XPATH, XPath.menuTabPath.format(num=idx)):
                click(driver, 5, By.XPATH, XPath.menuTab2Path.format(num=idx))
            while getElements(driver, 5, By.CLASS_NAME, ClassName.menuClass):
                click(driver, 5, By.XPATH, XPath.menuMoreButton)
            if getElements(driver, 5, By.CLASS_NAME, ClassName.deliveryClass):
                menuList = getElements(driver, 5, By.CLASS_NAME, ClassName.deliveryMenuNameClass)
                menuPrice = getElements(driver, 5, By.CLASS_NAME, ClassName.deliveryMenuPriceClass)
            elif getElements(driver, 5, By.CLASS_NAME, ClassName.takeOutMenuNameClass):
                menuList = getElements(driver, 5, By.CLASS_NAME, ClassName.takeOutMenuNameClass)
                menuPrice = getElements(driver, 5, By.CLASS_NAME, ClassName.deliveryMenuPriceClass)
            else:
                menuList = getElements(driver, 5, By.CLASS_NAME, ClassName.menuListClass)
                menuPrice = getElements(driver, 5, By.CLASS_NAME, ClassName.menuPriceClass)
            if not menuList:
                continue
            for menu_idx in range(len(menuList) - 1):
                data['menu'][menuList[menu_idx].text] = menuPrice[menu_idx].text
        if tab == '리뷰':
            # get Like
            if not click(driver, 5, By.XPATH, XPath.menuTabPath.format(num=idx)):
                if not click(driver, 5, By.XPATH, XPath.menuTab2Path.format(num=idx)):
                    click(driver, 5, By.XPATH, XPath.menuTab3Path.format(num=idx))
            while click(driver, 5, By.CLASS_NAME, ClassName.likeMoreClass):
                if getValue(driver, 5, By.CLASS_NAME, ClassName.likeMoreClass) != "더보기":
                    break
            time.sleep(0.5)
            likeTopic = getElements(driver, 5, By.CLASS_NAME, ClassName.likeTopicClass)
            if likeTopic:
                likeNum = getElements(driver, 5, By.CLASS_NAME, ClassName.likeNumClass)[1:]
                for idx in range(len(likeNum)):
                    data['like'][likeTopic[idx].text] = int(likeNum[idx].text.split('\n')[-1])
    driver.switch_to.parent_frame()
    return data
