from playwright.sync_api import sync_playwright
from datetime import datetime as dt
from datetime import timedelta as td
from time import sleep
import pandas as pd
import os

d,m,y = (dt.now()).strftime('%d'),(dt.now()).strftime('%m'),(dt.now()).strftime('%Y')

try:
    df_log = pd.read_excel('Normas\Log.xlsx',dtype={'Data':str})

    lista_palavras_chaves = ['Gestão de Capital','Risco de Crédito','Risco Operacional','Risco de liquidez']

    lista_link,lista_titulos = list(df_log['LINK']),list(df_log['TITULOS'])
except:]
    lista_palavras_chaves = ['Gestão de Capital',,'Risco de Crédito','Risco Operacional','Risco de liquidez']
    lista_link,lista_titulos = [],[]

with sync_playwright() as p:
                    browser = p.chromium.launch(headless=False)
                    page = browser.new_page()
                    lista_links,lista_titulo = [],[]
                    for x in lista_palavras_chaves:
                        link = f"https://www.bcb.gov.br/estabilidadefinanceira/buscanormas?conteudo={x.replace(' ','%20')}&dataInicioBusca=25%2F08%2F2023&dataFimBusca={d}%2F{m}%2F{y}&tipoDocumento=Todos"    
                        page.goto(link)
                        sleep(5)
                        try:
                            count = (page.locator('xpath=//div[@class="small" or @class="small ng-star-inserted"]').text_content()).split(' ')[2]
                            xz = 1
                            xy = 1
                            for y in range(int(count)):
                                link_enc = page.locator(f'xpath=//div[@class="encontrados" or @class="encontrados ng-star-inserted"]/ol/li[{xy}]/a').get_attribute('href')
                                link_enc = f'https://www.bcb.gov.br/{link_enc}'
                                if link_enc in lista_link:
                                    pass
                                elif link_enc in lista_links:
                                    pass
                                else:
                                    lista_link.append(link_enc)
                                    lista_links.append(link_enc)
                                    lista_titulo.append(page.locator(f'xpath=//div[@class="encontrados" or @class="encontrados ng-star-inserted"]/ol/li[{xy}]/a').text_content()),
                                    lista_titulos.append(page.locator(f'xpath=//div[@class="encontrados" or @class="encontrados ng-star-inserted"]/ol/li[{xy}]/a').text_content())
                                if xy == 15:
                                    page.goto(f'{link}&startRow={xz}')
                                    xz+=1
                                    xy=1
                                else:
                                    xz+=1
                                    xy+=1
                        except:
                            print(f'Sem novas normas para {x}')
                    browser.close()

(pd.DataFrame(list(zip(lista_link,lista_titulos)),columns=['LINK','TITULOS'])).to_excel('Normas\\Log.xlsx')
