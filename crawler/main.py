from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pickle


def loadDriver(driver_path: str):
    service = Service(driver_path)
    option = webdriver.ChromeOptions()
    option.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/101.0.4951.41 Safari/537.36')
    driver = webdriver.Chrome(service=service, options=option)
    return driver


def loadList(listPath: str) -> list:
    with open(listPath, 'rb') as fp:
        return pickle.load(fp)

if __name__ == '__main__':
    ########
    # fill #
    ########
    pass
