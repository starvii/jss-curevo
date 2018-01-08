#!/usr/bin/python
# -*- coding: utf-8 -*-

import json


def main():
    with open('../package.json', 'r') as f:
        j = json.load(f)
    cmds = list()
    if len(j['devDependencies'].keys()) > 0:
        savedev = ' '.join(j['devDependencies'].keys())
        cmds.append('npm install --save-dev {}'.format(savedev))
    if len(j['dependencies'].keys()) > 0:
        save = ' '.join(j['dependencies'].keys())
        cmds.append('npm install --save {};'.format(save))
    cmd = '; '.join(cmds)
    print(cmd)


if __name__ == '__main__':
    main()
