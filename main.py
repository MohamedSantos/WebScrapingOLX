import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
from difflib import SequenceMatcher
from selenium import webdriver
import time
from datetime import date

listJson = []

def search_data(pages=10, regiao='SP', marca='gm', modelo='meriva'):
    region_search = {'SP': 'sao-paulo-e-regiao'}
    prefix = {'SP': 'sp'}
    maker_search = {'': '', 'citroen': '/citroen', 'fiat': '/fiat', 'ford': '/ford', 'gm': '/gm-chevrolet',
                   'honda': '/honda', 'hyundai': '/hyundai'}
    model_search = {'': '', 'meriva': '/meriva'}
    for x in range(0, pages):
        print('LOOP NUMBER: ' + str(x))
        url = 'https://' + prefix[regiao] + '.olx.com.br/' + region_search[
            regiao] + '/autos-e-pecas/carros-vans-e-utilitarios' + maker_search[marca] + model_search[modelo] +\
              '?cf=1&pe=13000&ps=1000&rs=22'
        if x == 0 or x == 1:
            print('somente a primeira página')
        else:
            url = 'https://' + prefix[regiao] + '.olx.com.br/' + region_search[
                regiao] + '/autos-e-pecas/carros-vans-e-utilitarios' + \
                  maker_search[marca] + model_search[modelo] + '?cf=1&o=' + str(x) + '&pe=13000&ps=1000&rs=22'

        PARAMS = {
            "authority": "sp.olx.com.br",
            "method": "GET",
            "path": "/sao-paulo-e-regiao/autos-e-pecas/carros-vans-e-utilitarios",
            "scheme": "https",
            "referer": "https://sp.olx.com.br/sao-paulo-e-regiao/autos-e-pecas/carros-vans-e-utilitarios",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }
        page = requests.get(url=url, headers=PARAMS)
        soup = BeautifulSoup(page.content, 'lxml')
        itens = soup.find_all('li', {'class': 'sc-1fcmfeb-2'})

        for a in itens:
            try:
                name = a.findAll('h2')[0].contents[0]
                price = a.findAll('span', class_='sc-ifAKCX eoKYee')[0].contents[0]
                price = price.split('R$')[1]
                price = float(price.replace('.', ''))
                day_post = a.findAll('span', class_='wlwg1t-1 fsgKJO sc-ifAKCX eLPYJb')[0].contents[0]
                hour_post = a.findAll('span', class_='wlwg1t-1 fsgKJO sc-ifAKCX eLPYJb')[1].contents[0]
                url_post = a.find('a')['href']
                options = a.findAll('span', class_='sc-1j5op1p-0 lnqdIU sc-ifAKCX eLPYJb')[0].contents[0]
                options = options.strip()
                region = a.findAll('span', class_='sc-7l84qu-1 ciykCV sc-ifAKCX dpURtf')[0].contents[0]

                #print(f'Nome: {name} \n Preço: {price} \n Dia e hora: {day_post}-{hour_post} \n URL: {url_post} \n Adicionais: {options} \n Região: {region}')
                json = {'dia_postagem': day_post,
                        'hora_postagem': hour_post,
                        'nome': name,
                        'preco': price,
                        'url': url_post,
                        'opcoes': options,
                        'regiao': region
                        }
                listJson.append(json)
            except:
                print('anuncio')

search_data()
'''df = pd.DataFrame(listJson)
df.to_excel('veiculos.xlsx')'''
