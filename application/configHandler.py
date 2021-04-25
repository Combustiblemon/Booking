import configparser
import pathlib
configPath = f'{pathlib.Path(__file__).parent.absolute()}/config.ini'
config = configparser.ConfigParser()
config.read(configPath)

def getConfig():
    config = configparser.ConfigParser()
    config.read(configPath)
    
def writeConfig(category: str, variable_name: str, value):
    config[category][variable_name] = value
    with open(configPath, 'w') as configfile:
        config.write(configfile)