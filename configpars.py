import configparser


class ConfigParser:

    @staticmethod
    def configparser(name_api) -> str:
        config = configparser.ConfigParser()
        config.read('setting.ini')
        if name_api == 'VK':
            return config['VK_TOKEN']['TOKEN']


cfg = ConfigParser()
