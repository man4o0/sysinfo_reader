import xml
from xml.etree import ElementTree
import sys
import csv
import pprint
from collections import defaultdict

KEYS = ('Name', 'User', 'MB', 'CPU', 'GPU', 'Memory',
        'Disk 1',
        'Disk 1 size',
        'Disk 2',
        'Disk 2 size',
        'Disk 3',
        'Disk 3 size',
        'Disk 4',
        'Disk 4 size')

def main(argv):
    writer = csv.DictWriter(sys.stdout, fieldnames = KEYS)
    writer.writeheader()
    for a in argv:
        specs = parse(a)
        writer.writerow(specs)

def parse(a):
    root = ElementTree.parse(a)
    info = root.find('Category[@name="System Summary"]')
    specs = defaultdict(lambda: 'N/A')
    d = {}
    for child in info:
        key = child.find('Item')
        value = child.find('Value')
        if key is not None and value is not None:
            d[key.text] = value.text
    specs['Name'] = d['System Name']
    specs['CPU'] = d['Processor']
    specs['Memory'] = d['Installed Physical Memory (RAM)']
    specs['User'] = d['User Name']
    specs['MB'] = d['BaseBoard Manufacturer']
    root = ElementTree.parse(a)
    components = info.find('Category[@name="Components"]')
    display = components.find('Category[@name="Display"]')
    video = display.find('Data')
    specs['GPU'] = video.find('Value').text
    storage = components.find('Category[@name="Storage"]')
    disks = storage.find('Category[@name="Disks"]')
    disk = 0
    for child in disks:
        key = child.find('Item')
        value = child.find('Value')
        if key is None or value is None:
            continue
        if key.text == 'Model':
            disk += 1
            disk_key = 'Disk {0}'.format(disk)
            specs[disk_key] = value.text
        elif key.text == 'Size':
            specs[disk_key + ' size'] = value.text[:value.text.find('B')+1]
    return specs


if __name__ == '__main__':
    main(sys.argv[1:])
