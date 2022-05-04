from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pickle

from geopy.geocoders import Nominatim

from common.config import URL, XPath, Selector, ClassName
from common.util import *
from common.network import *

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

def getPlaceName():
    driver = load_driver('chromedriver.exe')
    name = set(getNamelist(driver=driver, sub_list=Subway))
    constructPickle('name_list', name)

def getPlaceInfo() :
    driver = loadDriver('chromedriver_win32/chromedriver.exe')
    geoLocal = Nominatim(user_agent='South Korea')
    placeList = loadList('./data/name_list.pkl')
    dataset, noPlace = [], []
    for name in placeList:
        if name == '7%칠백식당 신논현직영점': continue
        result = getPlaceInfoDetails(driver, geoLocal, name)
        if not result:
            noPlace.append(name)
        else:
            dataset.append(result)
    constructJson('./data/place_information', dataset)
    constructPickle('./data/no_place', noPlace)


if __name__ == '__main__':
    getPlaceInfo()

