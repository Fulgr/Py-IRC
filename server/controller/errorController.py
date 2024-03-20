import datetime

def log_error(error):
    with open('data/error.log', 'a', encoding='utf-8') as f:
        f.write(f'{datetime.datetime.now()}|{error}\n')