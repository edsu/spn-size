#!/usr/bin/env python3

# usage: collect.py <collection-id>

import re
import csv
import sys
import time
import internetarchive as ia

def main():
    if len(sys.argv) != 2:
        sys.exit("usage: collect.py <collection-id>")

    collection_id = sys.argv[1]

    sizes = {}
    last_size = 0
    for result in ia.search_items(f'collection:{collection_id}'):
        date, size = item_summary(result['identifier'])
        if date and size: 
            sizes[date] = sizes.get(date, 0) + size
            print(date, size, sizes[date])
        if len(sizes) > last_size:
            save(collection_id, sizes)
            last_size = len(sizes)

def item_summary(item_id, tries=1):
    try:
        item = ia.get_item(item_id)
    except Exception as e:
        print("caught exception", e)
        time.sleep(tries ** 2)
        return item_summary(item_id, tries=tries + 1)

    size = 0
    if 'files' not in item.item_metadata:
        return None, None

    for file in item.item_metadata['files']:
        if file['name'].endswith('arc.gz'):
            size += int(file['size'])

    m = re.match('^.+-(\d\d\d\d)(\d\d)(\d\d)', item.item_metadata['metadata']['identifier'])
    date = '%s-%s-%s' % m.groups()

    return date, size

def save(collection_id, sizes):
    dates = sorted(sizes.keys())
    writer = csv.writer(open(f'{collection_id}.csv', 'w'))
    writer.writerow(['date', 'bytes'])

    for date in dates:
        writer.writerow([date, sizes[date]])

if __name__ == "__main__":
    main()
