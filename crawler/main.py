from common.util import *
import pickle
import json
from selenium import webdriver
from common.config import URL, XPath, Selector, ClassName
from geopy.geocoders import Nominatim
from common.util import *


def loadDriver(driver_path: str):
    service = Service(driver_path)
    option = webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches", ["enable-logging"])
    option.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/101.0.4951.41 Safari/537.36')
    driver = webdriver.Chrome(service=service, options=option)
    return driver


def loadList(listPath: str) -> list:
    with open(listPath, 'rb') as fp:
        return pickle.load(fp)

# 리뷰 정보 모으기
def getReview(driver: webdriver, placeName: str):
    getReviewInfo(driver, placeName)


if __name__ == '__main__':
    # driver load
    driver = loadDriver('chromedriver_win32/chromedriver.exe')

    placeName = ['런치크라운 경기 수원시 영통구 대학1로8번길']

    for i in placeName:
        getReview(driver, i)
