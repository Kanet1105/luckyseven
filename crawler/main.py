from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pickle
from geopy.geocoders import Nominatim

from common.config import URL, XPath, Selector, ClassName
from common.util import *

def loadDriver(driverPath: str):
    service = Service(driverPath)
    option = webdriver.ChromeOptions()
    option.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/101.0.4951.41 Safari/537.36')
    driver = webdriver.Chrome(service=service, options=option)
    return driver

def loadList(listPath: str) -> list:
    with open(listPath, 'rb') as fp:
        return pickle.load(fp)


def getPlaceInfo(driver: webdriver, geoLocal: Nominatim, name: str) :
    data = placeInfoDict()

    # search the place
    driver.get(URL.baseURL.format(placeName=name))

    # switch to the search iframe
    switchToFrame(driver, 5, By.XPATH, XPath.searchIframe)
    # click the first fetched item
    click(driver, 5, By.XPATH, XPath.firstFetched)

    # switch to the entery iframe
    driver.switch_to.parent_frame()
    if not switchToFrame(driver, 5, By.XPATH, XPath.entryIframe) :
        print("No place : ", name)
        return None

    click(driver, 5, By.XPATH, XPath.homePath)
    # get place name, place type
    data['placeName'] = getElements(driver, 5, By.XPATH, XPath.placeName)[0].text
    data['placeType'] = getElements(driver, 5, By.XPATH, XPath.placeType)[0].text

    # get place mean rating
    num = 1
    placeMeanRating = getValue(driver, 5, By.XPATH, XPath.placeMeanRating)
    if placeMeanRating :
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
            description = getElements(driver, 5, By.XPATH, XPath.description.format(divNum1=5, divNum2=divNum, idx=index))
            if not description :
                description = getElements(driver, 5, By.XPATH, XPath.description.format(divNum1=6, divNum2=divNum, idx=index))
            if description :
                data['description'] = ' '.join(description[-1].text.split('내용 더보기')[0].split('\n'))

    scrollDown(driver)
    # get theme keyword
    if getElements(driver, 5, By.CLASS_NAME, ClassName.themeKeywordClass):
        themeData = getElements(driver, 5, By.CLASS_NAME, ClassName.themeDataClass)
        for value in themeData:
            data['themeKeywords'].append(value.text.split(', ')[-1])
    # get popularity
    tabList = getElements(driver, 5, By.XPATH, XPath.placeTab)
    if tabList :
        tabList = tabList[0].text.replace('\n', ' ').split(' ')
        if '메뉴' in tabList : divNum += 2
        else : divNum += 1
    else : tabList = []

    click(driver, 5, By.XPATH, XPath.datalabMoreButton.format(divNum=divNum))
    if getElements(driver, 5, By.CLASS_NAME, ClassName.popularityClass):
        for idx in range(10, 70, 10):
            data['agePopularity'][f'{idx}대'] = float(getValue(driver, 5, By.XPATH, XPath.agePopluarity.format(age=idx // 10)).replace('%', ''))
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
            if not menuList :
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

if __name__ == '__main__':
    driver = loadDriver('chromedriver_win32/chromedriver.exe')
    geoLocal = Nominatim(user_agent='South Korea')
    placeList = loadList('./data/name_list.pkl')

    result = getPlaceInfo(driver, geoLocal, '고기꾼김춘배 강남점')

    dataset, noPlace = [], []
    for name in placeList :
        if name == '7%칠백식당 신논현직영점' : continue
        result = getPlaceInfo(driver, geoLocal, name)
        if not result : noPlace.append(name)
        else :
            dataset.append(result)

    constructJson('./data/place_information', dataset)
    constructPickle('./data/no_place', noPlace)