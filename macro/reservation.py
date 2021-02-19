import time

from .functionContainer import FunctionContainer, EC, By, WebElement
from .untilDoDecorator import UntilDoDecorator
from .utils import *


class Reservation(FunctionContainer):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def reserve(self):
        try:
            self.login()
            self.select_date(date=get_date())
            self.select_time()
            self.insert_reservation_info()
            self.submit_reservation_info()
        except Exception as e:
            print("예약 중 오류가 발생하였습니다.\n프로그램을 종료합니다")
            raise e

    def login(self):
        """
        로그인 페이지로 이동하여 로그인한다.
        """
        url = self.config['urls']['login']
        login_selector = self.config['selectors']['login']
        login_value = self.config['values']['login']

        self.driver.get(url)
        self.driver.find_element_by_id(login_selector['id']['id']).send_keys(login_value['id'])
        self.driver.find_element_by_id(login_selector['password']['id']).send_keys(login_value['password'])
        self.driver.find_element_by_id(login_selector['button']['id']).click()

        self.alert_confirm()

    def select_date(self, date: datetime):
        """
        날짜를 받아서 해당 날짜의 예약 화면으로 이동한다.
        :param date: 선택하고자 하는 날짜
        url: query parameter 추가해야 한다. (txtStdDate=yyyy-mm-dd)
        """
        url = self.config['urls']['selectDate'] + "?txtStdDate={}".format(date.date().isoformat())
        nth_week, weekday = find_day_position(date)
        date_selector = ".calendar tbody > tr:nth-child({}) > td:nth-child({}) > .{}".format(nth_week+1, weekday, self.config['selectors']['date']['class'])

        self.wait_for_select_date(url, date_selector)
        self.alert_confirm()

    @UntilDoDecorator(0.3, "예약할 수 없습니다.")  # 0.3초 간격으로 가능할 때까지 진행한다.
    def wait_for_select_date(self, url: str, date_selector: str):
        """
        설정해놓은 날짜가 예약 가능할 때까지 반복해서 화면으로 이동을 시도한다.
        :param url: 날짜 선택하는 페이지 주소
        :param date_selector:
        """
        self.driver.get(url)
        self.driver.find_element_by_css_selector(date_selector).click()

    def select_time(self):
        """
        시간을 선택하여 예약 화면으로 이동한다.
        """
        try:
            timetable_el = self.wait_for_timetable()
            while True:
                reservation_times = timetable_el.find_elements_by_class_name(self.config['selectors']['time']['class'])
                self.select_time_in_reservation_table(reservation_times)
        except Exception as e:
            print("Select time Exception: ", e)

    def select_time_in_reservation_table(self, reservation_times):
        """
        예약 테이블에서 설정해놓은 가능한 시간 중 한 곳의 예약 화면으로 이동한다.
        :param reservation_times: List<WebElement>, 예약 가능한 시간표
        """
        for reservation_time in reservation_times:
            _reservation_info = self.config['values']['reservation']
            if reservation_time.get_attribute("hole") != _reservation_info['hole'] or \
                    not tim2int(_reservation_info['from']) <= tim2int(reservation_time.get_attribute("time")) < tim2int(
                        _reservation_info['to']):
                print("pass", reservation_time.get_attribute("time"), reservation_time.get_attribute("hole"))
                continue
            reservation_time.click()
            self.alert_confirm()
            if not self.alert_confirm():
                print(reservation_time.get_attribute("time"), reservation_time.get_attribute("hole"), "예약을 시작합니다.")

    def wait_for_timetable(self):
        """
        예약 가능 시간표가 로딩될 때까지 기다린다.
        최대 5초 기다리도록 설정 후 다시 1초로 되돌린다.
        """
        try:
            self.set_wait_time(is_max=True)
            timetable_el: WebElement = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, self.config['selectors']['time_table']['class'])))
        finally:
            self.set_wait_time(is_max=False)
        return timetable_el

    def insert_reservation_info(self):
        """
        동반자 입력, 개인정보 필수 수집 동의
        """
        for i in range(2, 5):
            names_selector = "#frm1 > table > tbody > tr:nth-child(6) > td > input:nth-child({})".format(i)
            name_el: WebElement = self.wait.until(EC.presence_of_element_located((By.SS_SELECTOR, names_selector)))
            name_el.send_keys(self.config["guests"]["guest{}".format(i)])
        self.driver.find_element_by_id(self.config['selectors']['check_agreement_private_info']['id']).click()  # 개인정보 필수 수집 동의
        time.sleep(2)

    def submit_reservation_info(self):
        """
        신청 완료
        """
        self.driver.find_element_by_id(self.config['selectors']['reservation_submit']['id']).click()
        print("DONE")

