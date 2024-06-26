import datetime

def error(error):
    with open('data/error.log', 'a', encoding='utf-8') as f:
        f.write(f'{datetime.datetime.now()}|{error}\n')

def log(message):
    with open('data/log.log', 'a', encoding='utf-8') as f:
        f.write(f'{datetime.datetime.now()}|{message}\n')
    print(message)