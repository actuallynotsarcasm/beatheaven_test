import json
import pandas as pd
import re


def replace_broken_symbols_title(item):
    item = item.lower()
    broken_symbols = list(filter(lambda y: int.from_bytes(y.encode()) > 10000, item)) + ['the ']
    for symbol in broken_symbols:
        item = item.replace(symbol, '')
    item = item.replace(' and ', '   ')
    return item


def replace_broken_symbols_metadata(item):
    broken_symbols = list(filter(lambda y: int.from_bytes(y.encode()) > 10000, item)) + ['the ']
    for symbol in broken_symbols:
        item = item.replace(symbol, '')
    item = item.replace(' and ', '   ')
    return item


def item_to_title_id(item):
    chars = ['&', '\'', '#', '[', ']', ';']
    title = f'{item['name']} - {item['artist']['name']}'
    title = title.lower()
    for char in chars:
        title = title.replace(char, ' ')
    title = title.strip()
    title = replace_broken_symbols_metadata(title)
    id = item['_id']
    return title, id


def mapping_hardfix(item):
    title, id = item
    hard_fixes = {
        'starfucker': 'strfkr',
        'sisq': 'sisqo',
        'psychic city (classixx remix)': 'psychic city - classixx remix',
        'empire ants': 'empire ants (feat. little dragon)',
        'hall   oates': 'daryl hall   john oates',
        'hold on loosely - .38 special': 'hold on loosely - 38 special',
        'd.a.n.c.e.': 'd.a.n.c.e',
        'ke$ha': 'kesha',
        'some kind of nature - gorillaz': 'some kind of nature (feat. lou reed) - gorillaz'
    }
    for old, new in hard_fixes.items():
        title = title.replace(old, new)
    return title, id


def mapping_afterfix(item):
    title, id = item
    feat_fix_pattern = re.compile(' \\(feat\\. .+\\)')
    title = feat_fix_pattern.sub('', title)
    return title, id


names = pd.read_csv('song_names.csv')

with open('tracks.json', 'r') as f:
    id_mapping = json.load(f)

id_mapping = dict(map(item_to_title_id, id_mapping))

names['title'] = names['0']
names['title'] = names['title'].map(replace_broken_symbols_title)
names['id'] = names['title'].map(id_mapping)
names.drop('0', axis=1, inplace=True)

broken_titles = names[names['id'].isna()].copy()
id_mapping = dict(map(mapping_hardfix, id_mapping.items()))
names.loc[broken_titles.index, 'id'] = broken_titles['title'].map(id_mapping)

broken_titles_2 = names[names['id'].isna()].copy()
id_mapping = dict(map(mapping_afterfix, id_mapping.items()))
names.loc[broken_titles_2.index, 'id'] = broken_titles_2['title'].map(id_mapping)

names['id'].to_csv('song_ids.csv', index=False)