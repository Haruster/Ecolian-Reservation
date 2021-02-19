"""
여기서 사용되지 않는 import들 다른 파일에서 사용됨
"""
from .driver import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class FunctionContainer:
    wait_for_element = 1
    wait_for_element_max = 5

    def __init__(self):
        self.driver = Driver.instance()
        self.wait = WebDriverWait(self.driver, self.wait_for_element)

    def alert_confirm(self):
        try:
            self.wait.until(EC.alert_is_present(), 'Timed out waiting for alerts to appear')
            alert = self.driver.switch_to.alert
            alert.accept()
            return True
        except Exception:
            print("알림창을 찾을 수 없습니다.")
            return False

    def set_wait_time(self, is_max: bool = False):
        self.wait = WebDriverWait(self.driver, self.wait_for_element_max if is_max else self.wait_for_element)
