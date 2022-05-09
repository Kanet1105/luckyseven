from common.util import *
from selenium.webdriver.chrome.service import Service
from common.network import *

# Driver load & get place list
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


# 장소 이름
def getPlaceName(driver:webdriver):
    name = set(getNamelist(driver=driver, sub_list=Subway))
    constructPickle('name_list', name)


# 리뷰 정보
def getReview(driver:webdriver):
    placeList = loadList('./data/name_list_all.pkl')
    for name, address in placeList:
        placeName = name + " " + address
        # result = getReviewInfo(driver, placeName, name, address)


# 장소 정보
def getPlaceInfo(driver:webdriver):
    geoLocal = Nominatim(user_agent='South Korea')
    placeList = loadList('./data/name_list_final.pkl')
    noPlace = []

    for name, address in placeList[20000:21000]:
        placeName = name + " " + address
        result = getPlaceInfoDetails(driver, geoLocal, placeName)
        if not result:
            noPlace.append(name)

    constructPickle('./data/no_place', noPlace)
    constructPickle('./data/resend_place', resend.PlaceInfoModel)
    constructPickle('./data/resend_review', resend.ReviewInfoModel)
    constructPickle('./data/resend_user', resend.UserInfoModel)


if __name__ == '__main__':
    driver = loadDriver('./chromedriver_win32/chromedriver.exe')
    getPlaceInfo(driver)
