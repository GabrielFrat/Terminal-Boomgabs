try:
    import bs4
    import pandas as pd
    import cfscrape
    import requests
    from time import sleep
    from selenium import webdriver
    from selenium.webdriver.common.by import By
except:
    print("Erro ao buscar notícias")


dictSites = {'InfoMoney Politica': 'https://www.infomoney.com.br/politica/', 
             'InfoMoney Economia':'https://www.infomoney.com.br/economia/', 
             'CNN Politica': 'https://www.cnnbrasil.com.br/politica/',
             'CNN Economia': 'https://www.cnnbrasil.com.br/economia/', 
             'Estadão Política': 'https://www.estadao.com.br/politica/',
             'Estadão Economia': 'https://www.estadao.com.br/economia/'}

class web_crawler:
    # inicializa o projeto
    def __init__(self, sites, navegador):
        self.dictSites = sites
        self.nav = navegador

    # busca as informações na web
    def scraping(self, site, link, nav):
        listAux = []
        listAuxLink = []
        try:
            nav.get(link)
            items = nav.find_elements(By.TAG_NAME, 'a')
            for i in items:
                href = i.get_attribute('href')
                text = i.text
                listAux.append(text)
                listAuxLink.append(href)
            sleep(5)
        except:
            print("Erro ao Assessar " + site)

        return listAux, listAuxLink

    # Executa limpeza e tratamento de dados
    def tratamento_dados(self):
        pass

    # Organiza e classifica as informações
    def organizador(self, listNames, listLinks):
        listNamesAux = []
        listLinksAux = []
        listKeys = []

        for i in listNames:
            for j in i:
                listNamesAux.append(j)

        for i in listLinks:
            for j in i:
                listLinksAux.append(j)

        for i in range(0, len(listLinksAux)):
            keys = str(listLinksAux[i]) + str(listNamesAux[i])
            listKeys.append(keys)

        dfLinks = pd.DataFrame()
        dfLinks['Nome'] = listNamesAux
        dfLinks['Link'] = listLinksAux
        dfLinks['Chave'] = listKeys
        
        dfLinks = dfLinks.loc[dfLinks['Nome'] != ""]
        dfLinks = dfLinks.loc[dfLinks['Link'] != ""]

        # Locar apenas noticias onde a vriavel seja maior que 20 caracteres
        dfLinks = dfLinks[dfLinks['Nome'].str.len() > 40]
        dfLinks = dfLinks.drop_duplicates(subset=['Link'])
        dfLinks.to_excel(r'C:\Users\gabri\OneDrive\Projetos\Extração de Noticias\data.xlsx')

    # Faz a execução completa do código
    def start(self):
        sites = self.dictSites
        navegador = self.nav
        #while True:
            # Traz o site e o seu link
        listSites = []
        listLinks = []
        for key, value in sites.items():
            site, link = starter.scraping(key, value, navegador)
            listLinks.append(link)
            listSites.append(site)
    
        starter.organizador(listSites, listLinks)

# instanciar o webdriver

options = webdriver.ChromeOptions()
navegador = webdriver.Chrome(options=options)
starter = web_crawler(dictSites, navegador)
starter.start()