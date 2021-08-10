import json
import re

with open('setting.json', mode='r', encoding='utf-8') as jfile:
    jdata = json.load(jfile)

CONFIG = {
    'TOKEN': jdata['TOKEN'],
    'CHANNEL_MAINROOM': jdata['CHANNEL_MAINROOM'],
    'CHANNEL_CODE': jdata['CHANNEL_CODE'],
    'SERVER': {},
    'CHANNEL_BOT': {},
    'CHANNEL_ROLE': {},
    'CHANNEL_EMOJI': {},
    'ESCAPE_START': jdata['ESCAPE_START'],
    'ESCAPE_FROZEN': jdata['ESCAPE_FROZEN'],
    'ESCAPE_END': jdata['ESCAPE_END'],
}

#  if re.match(r"")
pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
if re.match(pattern, CONFIG['ESCAPE_START']) is None \
        or re.match(pattern, CONFIG['ESCAPE_END']) is None \
        or re.match(pattern, CONFIG['ESCAPE_FROZEN']) is None:
    raise ValueError('ESCAPE_* should be YYYY-MM-dd HH:mm:ss')


for i in range(1, 10):
    CONFIG['CHANNEL_BOT'][i] = jdata[f'CHANNEL_BOT_{i}']
    CONFIG['SERVER'][i] = jdata[f'SERVER_{i}']
    CONFIG['CHANNEL_ROLE'][i] = jdata[f'CHANNEL_ROLE_{i}']
    CONFIG['CHANNEL_EMOJI'][i] = jdata[f'CHANNEL_EMOJI_{i}']
