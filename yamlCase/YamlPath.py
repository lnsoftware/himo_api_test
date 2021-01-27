import os

def ymlPath():
    return os.path.abspath(os.path.join(os.path.dirname(__file__)))

if __name__ == '__main__':
    path = ymlPath()
    path += '\\createOrder.yml'
    print(path)
