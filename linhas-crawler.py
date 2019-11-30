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
import unidecode
import logging
from bs4 import BeautifulSoup



def download_page(url, maxretries, timeout, pause):
    tries = 0
    htmlpage = None
    while tries < maxretries and htmlpage is None:
        try:
            url = unidecode.unidecode(url)
            with closing(urllib.request.urlopen(url, timeout=timeout)) as f:
                htmlpage = f.read()
                sleep(pause)
        except (urllib.error.URLError, socket.timeout, socket.error):
            tries += 1
    return htmlpage


def extract(basepath, outputfile_name):
    
    url = 'http://smtonline.pmmc.com.br/'

    counter = 0

    pagedir = os.path.join('data', 'pages', 'pagina')
    if not os.path.exists(pagedir):
        os.makedirs(pagedir)

    with open('./data/pages/json/linhas.json') as json_file:
        linhas = json.load(json_file)
        counter = 0
        for linha in linhas:
            try:
                htmlpage = download_page(linha['link'] + '_detalhada', 3, 180, 0.5)
                htmlpage = htmlpage.decode()
                with open(os.path.join(pagedir, 'linha' + str(counter) + '.html'), mode='w', encoding='utf-8') as f:
                    f.write(htmlpage)
                    print('linha' + str(counter) + '.html - file created')
                    counter += 1
            except:
                print('error Link:' + linha['link'])
    

def main():
    parser = argparse.ArgumentParser(description='Crawler of Steam game ids and names')
    parser.add_argument(
        '-i', '--input', help='Input file or path (all files in subpath are processed)', default='./data/pages/games',
        required=False)
    parser.add_argument(
        '-o', '--output', help='Output file', default='./data/games.csv', required=False)
    args = parser.parse_args()

    logging.basicConfig(filename='export.log',level=logging.DEBUG)


    extract(args.input, args.output)


if __name__ == '__main__':
    main()
