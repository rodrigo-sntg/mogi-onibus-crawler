#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2018 Andrea Esuli (andrea@esuli.it)
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import csv
import os
import re
import socket
import urllib
import urllib.request
from contextlib import closing
from time import sleep
import json
from bs4 import BeautifulSoup


def extract(basepath, outputfile_name):
    data = {}
    tudo = {}


    for root, _, files in os.walk(basepath):
        counter = 0
        for file in files:
            fullpath = os.path.join(root, file)
            with open(fullpath, encoding='utf8') as f:
                htmlpage = f.read()


                produto = {}

                try:
                    soup = BeautifulSoup(htmlpage, 'html.parser')
                    
                    _lis = soup.find('ul', {'id': 'myUL'}).find_all('a')
                    links = []

                    try:
                        for li in _lis:
                            ob = {}
                            ob['linha'] = li.text
                            ob['link'] = 'http://smtonline.pmmc.com.br/' + li.attrs['href']
                            links.append(ob)

                    except: print('erro contato')

                    
                    outputfile_name = './data/pages/json/linhas.json'
                    with open(outputfile_name, mode='w', encoding='utf-8', newline='') as outputfile:
                        json.dump(links, outputfile)

                except:
                    print('erro em ' + fullpath)
                    

def main():
    parser = argparse.ArgumentParser(description='Crawler of Steam  ids and names')
    parser.add_argument(
        '-i', '--input', help='Input file or path (all files in subpath are processed)', default='./data/pages/pagina',
        required=False)
    parser.add_argument(
        '-o', '--output', help='Output file', default='./data/produtos_extracted.json', required=False)
    args = parser.parse_args()

    extract(args.input, args.output)


if __name__ == '__main__':
    main()
