import configparser
import os

src = os.path.dirname(os.path.abspath(__file__))

settings =  {}

def read_config():
    config = configparser.ConfigParser()
    config.read(os.path.join(src,'config.ini'))

    global settings

    for section in config.sections():
        for key, val in config.items(section):
            settings[key] = val


read_config()



