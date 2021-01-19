#!/usr/bin/env python

import re
import csv
import internetarchive as ia

# TODO: make this script smart enough to not collect data already in spn2-size.csv

def item_summary(item_id):
    item = ia.get_item(item_id)

    size = 0
    if 'files' not in item.item_metadata:
        return None, None

    for file in item.item_metadata['files']:
        if file['name'].endswith('arc.gz'):
            size += int(file['size'])

    m = re.match('^spn2-(\d\d\d\d)(\d\d)(\d\d)', item.item_metadata['metadata']['identifier'])
    date = '%s-%s-%s' % m.groups()

    return date, size

sizes = {}
for result in ia.search_items('collection:save-page-now'):
    date, size = item_summary(result['identifier'])
    if date and size: 
        sizes[date] = sizes.get(date, 0) + size
        print(date, size, sizes[date])

dates = sorted(sizes.keys())
writer = csv.writer(open('spn2.csv', 'w'))
writer.writerow(['date', 'bytes'])

for date in dates:
    writer.writerow([date, sizes[date]])
