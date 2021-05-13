import configparser
import pathlib
configPath = f'{pathlib.Path(__file__).parent.absolute()}/config.ini'
config = configparser.ConfigParser()
config.read(configPath)

def getConfig() -> dict:
    global config
    config.read(configPath)
    return config
    
def writeConfig(category: str, variable_name: str, value):
    global config
    config[category][variable_name] = value
    with open(configPath, 'w') as configfile:
        config.write(configfile)