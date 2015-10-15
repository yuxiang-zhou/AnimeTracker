import configparser
config = configparser.ConfigParser()
config['DEFAULT'] = {
    'UpdatePeriod': 3600*12,
    'retry': 20
}
config['DATABASE'] = {
    'Server': 'localhost',
    'DBName': 'anime_storage',
    'Username': 'Developer',
    'Password': '1330871pp',
}
with open('service.config', 'w') as configfile:
    config.write(configfile)