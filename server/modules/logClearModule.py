import time

def start():
    while True:
        with open('data/log.log', 'w', encoding='utf-8') as f:
            f.write('')
        with open('data/error.log', 'w', encoding='utf-8') as f:
            f.write('')
        print('Log cleared')
        time.sleep(600)