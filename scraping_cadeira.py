# passo 1: pip install selenium

# Módulo para controlar o navegador web

from selenium import webdriver

# localizador de elementos

from selenium.webdriver.common.by import By

# Serviço para configurar o caminho do executável chromedriver

from selenium.webdriver.chrome.service import Service

# classe que permite executar ações avançadas, exemplo: mover o mouse, clique e arrasta, etc.

from selenium.webdriver.common.action_chains import ActionChains

# Classe que espera de forma explicita até queuma condição seja satisfeita exemplo: que um elemento apareça

from selenium.webdriver.support.ui import WebDriverWait

# Condições esperadas usadas com webdriverwait

from selenium.webdriver.support import expected_conditions as ec

# trabalhar com dataframe

import pandas as pd

# uso de funções relacionadas ao tempo 

import time 

# uso de tratamento de exeção

from selenium.common.exceptions import TimeoutException

# definir o caminho do chromedriver, chromedriver é o simulador do  navegador

chrome_driver_path = '"C:\Program Files\chromedriver-win64\chromedriver-win64\chromedriver.exe"'

# Configuração do webdriver

servico = Service(chrome_driver_path) # navegador controlado pelo selenium
opicoes = webdriver.ChromeOptions() # configurar as opções do navegador
opicoes.add_argument('--disable-gpu') # '--disable-gpu' = evita possiveis erros gráficos5
opicoes.add_argument('--window-size=1920,1080') # define uma resolução fixa

# inicialização do webdriver 

driver = webdriver.Chrome(service=servico, options=opicoes)

# definir a URL inicial

url_base = 'https://www.kabum.com.br/espaco-gamer/cadeiras-gamer'
driver.get(url_base)
time.sleep(5) # ele aguarda 5 segundos para garantir que a pág carregue

# criar um dicionario vazio para armazenar os nomes dos produtos e preços das cadeiras
dic_produtos = {'produto': [], 'preco': []}

# iniciar na pagina 1 e incrementar a cada troca de pagina
pagina = 1

while True:
    print(f'\n Coletando dados da página {pagina}...')
    
    try:
        # WebDriverWait(driver,10) = cria uma espera de até 10 segundos
        #untill = faz com que o código espere até que a condição seja verdadeira
        #ec.presence_of_all_elements_located(())  = verifica se todos os elementos 'productcard' estão acessiveis 
        # By.CLASS_NAME,'productCard' = indica que a busca será feita através da classe css
        
        WebDriverWait(driver,10).untill( 
            ec.presence_of_all_elements_located((By.CLASS_NAME,'productCard'))  
        )
        print('Elementos encontrados com sucesso')
    except TimeoutException:
        print('Tempo de espera excedido')
    
    produtos = driver.find_elements(By.CLASS_NAME, 'productCard')
    
    for produto in produtos:
        try:
            nome = produto.find_element(By.CLASS_NAME, 'nameCard').text.strip()
            preco = produto.find_element(By.CLASS_NAME, 'priceCard').text.strip()
            print(f'{nome} - {preco}')
            
            dic_produtos['produto'].append(nome)
            dic_produtos['preco'].append(preco)
        except Exception:
                print('Erro ao coletar dados:', Exception)
                
# Encontrar o acesso para a proxima pagina

# Fechar o navegador

# fazer o dataframe

# Salvar os dados em CSV(dataframe)