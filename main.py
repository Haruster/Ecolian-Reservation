import yaml

from macro import *


class Main:
    def __init__(self):
        self._init_config()

    def _init_config(self):
        with open('config.yaml', 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def run(self):
        _macro = Macro(self.config)
        _macro.run()


if __name__ == '__main__':
    main = Main()
    main.run()
