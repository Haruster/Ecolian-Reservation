from .driver import Driver
from .reservation import Reservation


class Macro:
    def __init__(self, config):
        self.config = config
        self.driver = Driver.instance()
        self.reservation = Reservation(self.config)

    def run(self):
        self.reservation.reserve()

    def quit(self):
        self.driver.close()
