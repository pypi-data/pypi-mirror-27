import json
import sys

class MyConfig:
    header = ''
    header2 = ''
    
    def __init__(self):
        print("init MyConfig")

    @classmethod
    def fromdict(cls, dictionary):
        objeto = cls();
        objeto.header = dictionary.get('header','')
        objeto.header2 = dictionary.get('header2','')
        return objeto
        
    @classmethod
    def leerConfig(cls):
        try:
            with open('config.json') as json_data_file:
                data = json.load(json_data_file)
            return MyConfig.fromdict(data)
        except :
            print("leerConfig except")
            return MyConfig()
    
    def escribirConfig(self):
        with open('config.json', 'w') as outfile:
            json.dump(self.__dict__, outfile)
