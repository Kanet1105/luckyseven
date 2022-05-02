from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# elements list 반환
def get_elements(driver: webdriver, timeout: int, kind: By, value: str) -> list:
    elements = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((kind, value))
    )
    return elements


# iframe 전환
def switch_to_frame(driver: webdriver, timeout: int, kind: By, value: str) -> bool:
    ack = WebDriverWait(driver, timeout).until(
        EC.frame_to_be_available_and_switch_to_it((kind, value))
    )
    return ack
