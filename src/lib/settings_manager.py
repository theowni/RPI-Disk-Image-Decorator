import os
from configparser import ConfigParser
from .emulate_manager import MNT_PATH


PATH = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(
    os.path.dirname(PATH), '.settings.ini'
)


class SettingsManager:
    def __init__(self, config_path=CONFIG_PATH):
        self.config = ConfigParser()
        self.config.read(CONFIG_PATH)

        if 'SETTINGS' not in self.config.sections():
            self.create_file()

    def set(self, key, value):
        self.config['SETTINGS'][key] = value
        self.save()

    def get(self, key):
        return self.config['SETTINGS'][key]

    def save(self):
        with open(CONFIG_PATH, 'w') as f:
            self.config.write(f)

    def create_file(self):
        self.config['SETTINGS'] = {
            'MNT_PATH': MNT_PATH,
        }
        self.save()
