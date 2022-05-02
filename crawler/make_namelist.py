from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time

sub_list = ['까치산',  '시청',  '을지로입구', '을지로3가', '을지로4가', '동대문역사문화공원', '신당', '상왕십리', '왕십리',  '한양대',  '뚝섬', '성수', '건대입구',
             '구의', '강변', '잠실나루', '잠실', '잠실새내', '종합운동장', '삼성', '선릉', '역삼', '강남', '교대', '서초', '방배', '사당', '낙성대', '서울대입구',
            '봉천', '신림', '신대방', '구로디지털단지', '대림', '신도림', '문래', '영등포구청', '당산', '합정', '홍대입구', '신촌', '이대', '아현', '충정로', '용답',
             '신답', '신설동', '도림천', '양천구청', '신정네거리', '용두',
             '강남', '양재', '양재시민의숲', '청계산입구', '판교', '정자', '미금', '동천', '수지구청', '성복', '상현', '광교중앙', '광교']

service = Service('chromedriver.exe')
option = webdriver.ChromeOptions()
option.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'
)
option.add_argument('headless')


all_name = []


service = Service('chromedriver.exe')
option = webdriver.ChromeOptions()
option.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'
)
option.add_argument('headless')


all_name = []


def get_data(name):
    driver = webdriver.Chrome(service=service, options=option)
    basePath = 'https://map.kakao.com/'
    driver.get(basePath)
    name_list = []
    # 한번 클릭해야 다른 요소에 접근 가능 (팝업창 제거)
    sheild = '//*[@id="dimmedLayer"]'
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, sheild))).click()

    # 검색어 입력 ex. oo역 음식점
    search_path = '//*[@id="search.keyword.query"]'
    search = '{}역 음식점'

    search_box = driver.find_element(By.XPATH,search_path)
    actions = ActionChains(driver).send_keys_to_element(search_box, search.format(name)).send_keys(Keys.ENTER)
    actions.perform()

    ##  장소더보기 클릭 (모든 페이지 접근 위해)
    more = '//*[@id="info.search.place.more"]'
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, more))).click()

    # 총 장소 수 & 눌러야하는 장소더보기 버튼 수
    place_cnt = int(driver.find_element(By.XPATH, value='//*[@id="info.search.place.cnt"]').text.replace(',',''))
    click_cnt = 7
    # place_cnt//15//5//5

    # 페이지마다 모든 음식점 리스트 가져오기
    try:
        for _ in range(click_cnt):
            for no in range(1,6):
                # driver.find_element(By.XPATH, value=f'//*[@id="info.search.page.no{no}"]').click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="info.search.page.no{no}"]'))).click()
                time.sleep(0.5)
                names = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'link_name')))
                for _ in names:
                    name = _.text
                    if name not in name_list:
                        name_list.append(name)
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="info.search.page.next"]'))).click()
    # 없는 페이지면
    except:
        driver.quit()
        return name_list
                
            
            
            
    driver.quit()
    return name_list
    
if __name__ == '__main__':
    for sub in sub_list:
        print(sub)
        all_name += get_data(sub)
