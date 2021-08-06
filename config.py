import json

with open('setting.json', mode='r', encoding='utf-8') as jfile:
    jdata = json.load(jfile)

CONFIG = {
    'TOKEN': jdata['TOKEN'],
    'CHANNEL_MAINROOM': jdata['CHANNEL_MAINROOM'],
    'CHANNEL_BOT': {},
    'CHANNEL_ROLE': {},
    'CHANNEL_EMOJI': {},
}

for i in range(1, 10):
    CONFIG['CHANNEL_BOT'][i] = jdata[f'CHANNEL_BOT_{i}']
    CONFIG['CHANNEL_ROLE'][i] = jdata[f'CHANNEL_ROLE_{i}']
    CONFIG['CHANNEL_EMOJI'][i] = jdata[f'CHANNEL_EMOJI_{i}']
