from config import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import traceback


class Crawler:
    def __init__(self):
        self.chrome = Service('D:\\PythonProjects\\L7D\\chromedriver_win32\\chromedriver.exe')
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36')
        self.driver = webdriver.Chrome(service=self.chrome, options=self.option)
        self.dataset = []

    def waitForObject(self, kind: str, path: str):
        if kind == 'iframe':
            WebDriverWait(self.driver, 5).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, path))
            )

        elif kind == 'element':
            element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, path))
            )
            return element

    def getText(self, path: str):
        placeName = self.waitForObject('element', path)
        print(placeName.text)

    def construct(self):
        

    def search(self, placeName: str):
        try:
            # get the url and switch to the search frame
            # wait for the element to be located and click the element
            self.driver.get(Path.baseURL.format(placeName=placeName))
            self.waitForObject('iframe', Path.searchIframe)
            firstFetched = self.waitForObject('element', Path.firstFetched)
            firstFetched.click()

            # switch to the entry frame and construct data
            self.driver.switch_to.parent_frame()
            self.waitForObject('iframe', Path.entryIframe)

            # construct json
            self.construct()
        except:
            print(traceback.format_exc())


if __name__ == '__main__':
    crawler = Crawler()
    crawler.search('가보정')
