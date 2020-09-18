#!/usr/bin/env python3

import json, csv

ioc_list = []
iocs = {
    'filenames':[''],
    'hashes':[''],
    'ipv6':[''],
    'ipv4':['']
}

with open("otx-filename-iocs.txt") as f:
    filename = f.read()
    lines = filename.splitlines()
    reader = csv.reader(lines, delimiter=",")
    for row in reader:
        ioc_list.append(row)
    for value in ioc_list:
        iocs['filenames'].append(value[0])
    with open("otx-filename-iocs.json", "w") as outfile:
        json.dump(ioc_list, outfile, indent=4, sort_keys=True)
with open("otx-hash-iocs.txt") as h:
    ioc_list = []
    hash = h.read()
    lines = hash.splitlines()
    reader = csv.reader(lines, delimiter=",")
    for row in reader:
        ioc_list.append(row)
    for value in ioc_list:
        iocs['hashes'].append(value[0])
    with open("otx-hash-iocs.json", "w") as outfile:
        json.dump(ioc_list, outfile, indent=4, sort_keys=True)
with open("otx-c2-iocs-ipv6.txt") as c:
    ioc_list = []
    ipv6 = c.read()
    lines = ipv6.splitlines()
    reader = csv.reader(lines, delimiter=",")
    for row in reader:
        ioc_list.append(row)
    for value in ioc_list:
        iocs['ipv6'].append(value[0])
    with open("otx-c2-iocs-ipv6.json", "w") as outfile:
        json.dump(ioc_list, outfile, indent=4, sort_keys=True)
with open("otx-c2-iocs-ipv4.txt") as i:
    ioc_list = []
    ipv4 = i.read()
    lines = ipv4.splitlines()
    reader = csv.reader(lines, delimiter=",")
    for row in reader:
        ioc_list.append(row)
    for value in ioc_list:
        iocs['ipv4'].append(value[0])
    with open("otx-c2-iocs-ipv4.json", "w") as outfile:
        json.dump(ioc_list, outfile, indent=4, sort_keys=True)
#print(json.dumps(iocs, indent=4))
