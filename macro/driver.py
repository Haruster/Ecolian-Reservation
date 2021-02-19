from selenium import webdriver


class SingletonInstance:
    __instance = None

    @classmethod
    def __get_instance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kwargs):
        cls.__instance = cls(*args, **kwargs)
        cls.instance = cls.__get_instance
        return cls.__instance


class Driver(webdriver.Firefox, SingletonInstance):
    def __init__(self, **kwargs):
        self.driver = super(Driver, self).__init__(**kwargs)
