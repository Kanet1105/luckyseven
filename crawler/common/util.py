import pickle
import json
import time
import traceback
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from geopy.geocoders import Nominatim
from .config import *
from .network import *


# element 여러개 반환
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
def search(driver: webdriver, keyword: str):
    search_path = XPath.searchPathKakao
    search_box = getElements(driver, 0.5, By.XPATH, search_path)
    actions = ActionChains(driver).send_keys_to_element(search_box[0], keyword).send_keys(Keys.ENTER)
    actions.perform()


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
    click(driver, 1, By.XPATH, XPath.sheild)
    time.sleep(1)
    search(driver, sub + "역 맛집")  # 검색어 입력
    click(driver, 1, By.XPATH, XPath.more)  ##  장소더보기 클릭 (모든 페이지 접근 위해)


# 모든 페이지 정보 불러오기
def getPageList(driver: webdriver, no):
    nameList = []
    time.sleep(1)
    click(driver, 1, By.XPATH, XPath.pageNo.format(no), )  # 페이지 클릭
    time.sleep(1)
    name = getElements(driver, 1, By.CLASS_NAME, ClassName.place_kakao)  # 페이지 내 모든 음식점 리스트 반환
    address = getElements(driver, 1, By.CLASS_NAME, ClassName.addr_kakao)  # 페이지 내 모든 음식점 주소 반환
    for i in range(len(name)):
        if name[i].text not in nameList:
            nameList.append((name[i].text.replace('%', '%20'), " ".join(address[i].text.split()[:4])))
            # print((name[i].text, " ".join(address[i].text.split()[:4])))  # 디버깅위해 출력
    return nameList


# 지하철 목록에서 모든 음식점이름 반환
def getNamelist(driver: webdriver, sub_list):
    all_list = []
    try:
        for sub in sub_list:
            # print(sub) # 디버깅 위해 출력
            getSuburl(driver, sub)
            for _ in range(7):
                for no in range(1, 6):
                    all_list += getPageList(driver, no)
                click(driver, 5, By.XPATH, XPath.nextPage)  # 다음페이지 클릭
        return all_list
    except:
        print(traceback.format_exc())
        return all_list


# div num 확인하기
def countDivNum(driver: webdriver):
    divNum = 1
    if getElements(driver, 5, By.CLASS_NAME, ClassName.zeroClass):
        divNum += 1
    if getElements(driver, 5, By.CLASS_NAME, ClassName.announcementClass):
        divNum += 1
    return divNum


# 영업 시간 더보기 버튼 클릭
def clickTimeMoreButton(driver: webdriver):
    if not click(driver, 5, By.XPATH, XPath.timeMoreButton.format(divNum=divNum, idx=index)):
        if not click(driver, 5, By.XPATH, XPath.timeMoreButton2.format(divNum=divNum, idx=index)):
            click(driver, 5, By.XPATH, XPath.timeMoreButton3.format(divNum=divNum, idx=index))


# 메뉴 정보 받아오기
def getMenuInfo(driver):
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
    return menuList, menuPrice


# 리뷰 탭 클릭하기
def clickTab(driver: webdriver, name: str):
    tabElements = getElements(driver, 5, By.CLASS_NAME, ClassName.reviewTabClass)

    for i, j in enumerate(tabElements):
        if j.text == name:
            click(driver, 5, By.XPATH, XPath.reviewTab.format(index=i + 1))
            return True

    return False


# 리뷰 최신 순으로 정렬하기 버튼
def clickRecent(driver: webdriver):
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
        element1 = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((kind, value1)))
        userInfo['userHash'] = element1.get_attribute('href').split('/')[-2]
        userInfo['review'] = 0
        userInfo['photo'] = 0
        userInfo['following'] = 0
        userInfo['follower'] = 0
        # 포함된 user의 정보 가져오기
        element2 = getElements(element1, timeout, kind, value2)
        if element2 != None:
            for i in element2:
                info = i.text.split(' ')
                userInfo[info[0]] = int(info[1])  # ex. userInfo['리뷰'] = 1244

        return userInfo
    except:
        return None


def getReviewSubInfo(driver: webdriver, timeout: int, kind: By, value1: str, value2: str):
    reviewInfo = dict()
    reviewInfo['visitDay'] = None
    reviewInfo['visitCount'] = 0
    reviewInfo['score'] = None
    try:
        element1 = getElements(driver, timeout, kind, value1)[0] #WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((kind, value1)))
        element2 = getElements(element1, timeout, kind, value2)  ###############

        if element2:
            for i in element2:
                if '방문일' in i.text:
                    reviewInfo['visitDay'] = i.text.split('\n')[1]
                if '번째' in i.text:
                    num = i.text.split('\n')[0].strip('번째 방문')
                    if num.isdigit():
                        reviewInfo['visitCount'] = int(num)
                    else:
                        reviewInfo['visitCount'] = -1
                if '별점' in i.text:
                    reviewInfo['score'] = i.text.split('\n')[1]
        return reviewInfo
    except:
        return None


def getReviewInfo(driver: webdriver, placeName: str, address: str, prevNum: int):
    # print(placeName) # 디버깅 위한 출력
    # 최신순 버튼 클릭
    clickRecent(driver)

    finish = False
    while True :
        # 현재 페이지 리뷰 element들 가져오기
        scrollDown(driver)
        reviewElements = getElements(driver, 10, By.CLASS_NAME, ClassName.reviewClass)
        if reviewElements:
            # 각 리뷰에서 정보 가져오기
            for i in range(prevNum, len(reviewElements)):
                pl = Payload()
                reviewData = pl.reviewInfo
                userData = pl.userInfo
                click(reviewElements[i], 5, By.CLASS_NAME, ClassName.reviewMoreContentButtonClass)

                # 리뷰 유저의 ID -> str
                reviewUserId = getValue(reviewElements[i], 5, By.CLASS_NAME, ClassName.reviewUserId)
                if reviewUserId == None:
                    continue

                # 리뷰 유저에 대한 정보 -> dict
                reviewUserHash = getHashValue(reviewElements[i], 1, By.CLASS_NAME, ClassName.reviewUserHash1,ClassName.reviewUserHash2)
                # 리뷰 내용 -> str
                reviewContent = getValue(reviewElements[i], 1, By.CLASS_NAME, ClassName.reviewContent)
                # review 별점, 방문날짜, 방문 횟수 - dict
                reviewInfo = getReviewSubInfo(reviewElements[i], 1, By.CLASS_NAME, ClassName.reviewInfo1, ClassName.reviewInfo2)

                # 올해 리뷰가 아니면 break
                if reviewInfo:
                    if len(reviewInfo['visitDay'].split('.')) != 3:
                        finish = True
                        break

                # 중복 상관없이 유저 정보 저장
                userData['userHash'] = reviewUserHash['userHash']
                userData['userID'] = reviewUserId
                userData['reviewNum'] = reviewUserHash['review']
                userData['photo'] = reviewUserHash['photo']
                userData['following'] = reviewUserHash['following']
                userData['follower'] = reviewUserHash['follower']

                reviewData['userHash'] = reviewUserHash['userHash']
                reviewData['reviewUserID'] = reviewUserId
                reviewData['placeName'] = placeName
                reviewData['placeAddress'] = address
                reviewData['reviewContent'] = reviewContent
                reviewData['reviewInfoScore'] = reviewInfo['score']
                reviewData['reviewInfoVisitDay'] = reviewInfo['visitDay']
                reviewData['reviewInfoVisitCount'] = reviewInfo['visitCount']

                # print(reviewData) # 디버깅을 위한 출력
                sendData("ReviewInfoModel", reviewData)
                sendData("UserInfoModel", userData)
        prevNum = len(reviewElements)
        if finish or not click(driver, 2, By.CLASS_NAME, ClassName.reviewMoreButtonClass):
            break


def loadPlacePage(driver: webdriver):
    # switch to the search iframe
    switchToFrame(driver, 5, By.XPATH, XPath.searchIframe)

    # click the first fetched item
    click(driver, 5, By.XPATH, XPath.firstFetched)

    # switch to the entery iframe
    driver.switch_to.parent_frame()
    if not switchToFrame(driver, 5, By.XPATH, XPath.entryIframe):
        return False
    return True


def getPlaceInfoDetails(driver: webdriver, geoLocal: Nominatim, name: str):
    pl = Payload()
    data = pl.placeInfo

    # search the place
    driver.get(URL.baseURL.format(placeName=name))

    if not loadPlacePage(driver):
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

    divNum = countDivNum(driver)

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
        if '메뉴' in tabList: divNum += 2
        else: divNum += 1

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

    if clickTab(driver, '메뉴'):
        menuList, menuPrice = getMenuInfo(driver)
        if menuList :
            for menu_idx in range(len(menuList) - 1):
                data['menu'][menuList[menu_idx].text] = menuPrice[menu_idx].text

    driver.refresh()
    loadPlacePage(driver)
    if clickTab(driver, '리뷰'):  # get Like
        while click(driver, 5, By.CLASS_NAME, ClassName.likeMoreClass):
            if getValue(driver, 5, By.CLASS_NAME, ClassName.likeMoreClass) != "더보기": break

        time.sleep(0.5)
        likeTopic = getElements(driver, 5, By.CLASS_NAME, ClassName.likeTopicClass)
        if likeTopic:
            likeNum = getElements(driver, 5, By.CLASS_NAME, ClassName.likeNumClass)[1:]
            for idx in range(len(likeNum)):
                data['like'][likeTopic[idx].text] = int(likeNum[idx].text.split('\n')[-1])

    sendData("PlaceInfoModel", data)
    print(data)
    getReviewInfo(driver, data['placeName'], data['placeAddress'], len(data['like']))

    driver.switch_to.parent_frame()
