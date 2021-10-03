#!/usr/bin/env python3

# usage: collect.py <collection-id>

import re
import csv
import sys
import internetarchive as ia

def item_summary(item_id):
    item = ia.get_item(item_id)

    size = 0
    if 'files' not in item.item_metadata:
        return None, None

    for file in item.item_metadata['files']:
        if file['name'].endswith('arc.gz'):
            size += int(file['size'])

    m = re.match('^.+-(\d\d\d\d)(\d\d)(\d\d)', item.item_metadata['metadata']['identifier'])
    date = '%s-%s-%s' % m.groups()

    return date, size

if len(sys.argv) != 2:
    sys.exit("usage: collect.py <collection-id>")

collection_id = sys.argv[1]

sizes = {}
for result in ia.search_items(f'collection:{collection_id}'):
    date, size = item_summary(result['identifier'])
    if date and size: 
        sizes[date] = sizes.get(date, 0) + size
        print(date, size, sizes[date])

dates = sorted(sizes.keys())
writer = csv.writer(open(f'{collection-id}.csv', 'w'))
writer.writerow(['date', 'bytes'])

for date in dates:
    writer.writerow([date, sizes[date]])
