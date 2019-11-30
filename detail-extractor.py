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
from lxml import etree


def extract(basepath, outputfile_name):
    data = {}
    tudo = {}

    games = dict()

    # counter = 0
    tudo['todos'] = []
    data['cervejarias'] = []

    linhas = []

    for root, _, files in os.walk(basepath):
        counter = 0
        for file in files:
            fullpath = os.path.join(root, file)
            with open(fullpath, encoding='utf8') as f:
                htmlpage = f.read()

                htmlpage = htmlpage.replace('th', 'td')


                linha = {}

                try:
                    soup = BeautifulSoup(htmlpage, 'html.parser')
                    
                    
                    _tables = soup.find_all(lambda tag: tag.name=='table')
                    # table1 = soup.html.body.div.nextSibling.table[1]


                    # _tables = soup.find('div', {'class' : 'mt-2 container div_regular'}).find_all(lambda tag: tag.name=='table')
                    _title = soup.find_all(lambda tag: tag.name=='h1')
                    _detail = soup.find('div', {'class' : 'mt-2 container div_regular'})
                    links = []
                    titulo = _title[0].text
                    detalhe = _detail.text
                    linha['titulo'] = titulo
                    linha['detalhe'] = detalhe
                    linha['viagens'] = {}
                    linha['ida'] = []
                    linha['volta'] = []
                    linha['viagens']['diaUtil'] = []
                    linha['viagens']['sabado'] = []
                    linha['viagens']['domingo'] = []
                    
                    try:
                        table = _tables[0]
                        _rows = table.findAll(lambda tag: tag.name=='tr')
                        for row in _rows:
                            _cols = row.findAll('td')
                            viagem = {}

                            viagem['numero'] = _cols[0].text
                            viagem['pontoA'] = _cols[2].text
                            viagem['pontoB'] = _cols[4].text

                            linha['viagens']['diaUtil'].append(viagem)

                    except: print(titulo)

                    try:
                        table = _tables[1]
                        _rows = table.findAll(lambda tag: tag.name=='tr')
                        for row in _rows:
                            _cols = row.findAll('td')
                            viagem = {}

                            viagem['numero'] = _cols[0].text
                            viagem['pontoA'] = _cols[2].text
                            viagem['pontoB'] = _cols[4].text

                            linha['viagens']['sabado'].append(viagem)

                    except: print(titulo)

                    try:
                        table = _tables[2]
                        _rows = table.findAll(lambda tag: tag.name=='tr')
                        for row in _rows:
                            _cols = row.findAll('td')
                            viagem = {}

                            viagem['numero'] = _cols[0].text
                            viagem['pontoA'] = _cols[2].text
                            viagem['pontoB'] = _cols[4].text

                            linha['viagens']['domingo'].append(viagem)
                    except: print(titulo)
                    
                    try:
                        table = _tables[3]
                        _rows = table.findAll(lambda tag: tag.name=='tr')
                        itinerario = []
                        for row in _rows:
                            _cols = row.findAll('td')

                            itinerario.append(_cols[0].text)

                        linha['ida'] = itinerario

                    except: print(titulo)

                    try:
                        table = _tables[4]
                        _rows = table.findAll(lambda tag: tag.name=='tr')
                        itinerario = []
                        for row in _rows:
                            _cols = row.findAll('td')

                            itinerario.append(_cols[0].text)

                        linha['volta'] = itinerario

                    except: print(titulo)


                    linhas.append(linha)

                except:
                    print('erro em ' + fullpath)
                    
    outputfile_name = './data/pages/json/linhas_detail.json'
    with open(outputfile_name, mode='w', encoding='utf-8', newline='') as outputfile:
        json.dump(linhas, outputfile)

def main():
    parser = argparse.ArgumentParser(description='Crawler of Steam game ids and names')
    parser.add_argument(
        '-i', '--input', help='Input file or path (all files in subpath are processed)', default='./data/pages/pagina',
        required=False)
    parser.add_argument(
        '-o', '--output', help='Output file', default='./data/produtos_extracted.json', required=False)
    args = parser.parse_args()

    extract(args.input, args.output)


if __name__ == '__main__':
    main()
