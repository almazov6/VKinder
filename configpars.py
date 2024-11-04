import configparser


class ConfigParser:

    @staticmethod
    def configparser(name_api) -> str:
        config = configparser.ConfigParser()
        config.read('setting.ini')
        if name_api == 'VK':
            return config['VK_TOKEN']['TOKEN']
        if name_api == 'SVK':
            return config['SERVICE_TOKEN']['TOKEN']
        if name_api == 'USR':
            return config['USER_TOKEN']['TOKEN']


cfg = ConfigParser()
