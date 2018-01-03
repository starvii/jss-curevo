#!/usr/bin/python
# -*- coding: utf-8 -*-

""" by starvii"""

import json


def main():
    with open('../package.json', 'r') as f:
        j = json.load(f)
    savedev = ' '.join(j['devDependencies'].keys())
    save = ' '.join(j['dependencies'].keys())
    cmd = 'npm install --save-dev {}; npm install --save {};'.format(savedev, save)
    print(cmd)

if __name__ == '__main__':
    main()
