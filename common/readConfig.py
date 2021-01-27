import configparser

file = '../conf/config.ini'
def getConfigName():
    con = configparser.ConfigParser()
    con.read(file, encoding='utf-8')
    configName = con.sections()
    configName = tuple(configName)
    return configName

def orderDataBase():
    con = configparser.ConfigParser()
    con.read(file, encoding='utf-8')
    configName = getConfigName()
    for i in range(0,len(configName)):
        if configName[i]=='OrderBase':
            c = dict(con.items(configName[0]))
            return c['host'],c['port'],c['user'],c['password'],c['db']

def cityDataBase():
    con = configparser.ConfigParser()
    con.read(file,encoding='utf-8')
    configName = getConfigName()



if __name__ == '__main__':
    rf = configparser.ConfigParser()
    try:
        rf.read(file,encoding='utf-8')
        result = rf.get("OrderBase","host")
        print(result)
    except:
        pass