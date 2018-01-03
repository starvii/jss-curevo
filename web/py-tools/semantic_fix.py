#!/usr/bin/python
# -*- coding: utf-8 -*-

""" by starvii"""

from distutils.log import warn as printf
from shutil import copyfile, rmtree
import os


def main():
    """
由于 semantic-ui 配置文件问题，
对 webpack 兼容性不好。

此脚本修改几个存在问题的配置文件，
运行之后即可使用 webpack 加载  semantic-ui
"""
    try:
        os.remove('../semantic.json')
    except Exception:
        printf('delete [semantic.json] failed.')
    try:
        rmtree('../semantic')
    except Exception:
        printf('delete [semantic] failed.')

    try:
        src = r'../node_modules/semantic-ui/src/theme.config.example'
        tar = r'../node_modules/semantic-ui/src/theme.config'
        copyfile(src, tar)
    except Exception:
        pass

    config_files = [
        r'../node_modules/semantic-ui/src/themes/default/globals/site.variables',
        r'../node_modules/semantic-ui/src/themes/flat/globals/site.variables',
        r'../node_modules/semantic-ui/src/themes/material/globals/site.variables',
    ]

    for filename in config_files:
        with open(filename, 'r') as file:
            lines = file.readlines()
        writelines = []
        for line in lines:
            if line.strip().startswith(r'@importGoogleFonts'):
                writelines.append(r'@importGoogleFonts : false;' + os.linesep)
                continue
            if line.strip().startswith('@fontPath'):
                writelines.append(line.replace(r'../../themes/', r'../../../themes/'))
                continue
            writelines.append(line)
        with open(filename, 'w') as file:
            file.writelines(writelines)


if __name__ == '__main__':
    main()
