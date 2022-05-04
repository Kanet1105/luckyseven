from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pickle
from common.util import *
from common.config import *

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



if __name__ == '__main__':
    getPlaceName()
    ########
    # fill #
    ########
    pass
