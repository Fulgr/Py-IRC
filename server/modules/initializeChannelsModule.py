import utils.channelUtil as channelUtil
import json

def start():
    with open('data/channels.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    for channel in data:
        channelUtil.Channel(channel)