from selenium import webdriver  # Importa o módulo principal do Selenium para automação de navegador
from selenium.webdriver.common.by import By  # Permite localizar elementos por diferentes métodos (como ID, classe, etc.)
from selenium.webdriver.chrome.service import Service  # Permite configurar o serviço do ChromeDriver
from selenium.webdriver.common.action_chains import ActionChains  # Permite executar ações encadeadas no navegador (não utilizado no código)
from selenium.webdriver.support.ui import WebDriverWait  # Permite criar uma espera explícita até que condições sejam atendidas
from selenium.webdriver.support import expected_conditions as ec  # Define as condições esperadas para a espera explícita
import pandas as pd  # Importa o pandas para manipulação e salvamento de dados em tabela
import time  # Importa funções relacionadas ao tempo, como pausas com sleep
from selenium.common.exceptions import TimeoutException  # Importa exceção usada caso uma espera exceda o tempo limite

caminho_driver = r"C:\Program Files\chromedriver-win64\chromedriver-win64\chromedriver.exe"  
# Define o caminho onde está instalado o ChromeDriver no sistema

servico = Service(caminho_driver)  
# Cria um serviço do ChromeDriver com o caminho definido

controle = webdriver.ChromeOptions()  
# Cria uma instância de opções de configuração para o navegador Chrome

controle.add_argument('--disable-gpu')  
# Adiciona um argumento para desativar o uso de GPU, útil para compatibilidade

controle.add_argument('--window-size=1920,1080')  
# Define o tamanho da janela do navegador para uma resolução específica

executador = webdriver.Chrome(service=servico, options=controle)  
# Inicia o navegador Chrome com o serviço e as configurações definidas

url_site = 'https://www.kabum.com.br/espaco-gamer/cadeiras-gamer'  
# Define a URL do site que será acessado

executador.get(url_site)  
# Faz o navegador acessar a URL definida

time.sleep(5)  
# Aguarda 5 segundos para garantir que a página seja carregada

produtos = {'titulo': [], 'preco': []}  
# Cria um dicionário vazio para armazenar os títulos e preços dos produtos

pagina_atual = 1  
# Inicializa a variável para controlar o número da página atual

while True:  # Inicia um loop infinito que será encerrado manualmente dentro do código
    print(f'\n Coletando dados da página {pagina_atual}...')  # Informa a página sendo processada
    
    try:
        WebDriverWait(executador, 10).until(
            ec.presence_of_all_elements_located((By.CLASS_NAME, 'productCard'))
        )  # Espera até que todos os elementos com a classe 'productCard' estejam presentes na página
        print('Elementos encontrados com sucesso')  # Confirma que os elementos foram encontrados
    except TimeoutException:
        print('Tempo de espera excedido')  # Informa que o tempo de espera terminou antes de os elementos carregarem

    elementos = executador.find_elements(By.CLASS_NAME, 'productCard')  
    # Coleta todos os elementos da página com a classe 'productCard'

    for produto in elementos:  # Itera por cada produto encontrado
        try:
            nome = produto.find_element(By.CLASS_NAME, 'nameCard').text.strip()  
            # Coleta e limpa o texto do nome do produto
            preco = produto.find_element(By.CLASS_NAME, 'priceCard').text.strip()  
            # Coleta e limpa o texto do preço do produto
            print(f'{nome} - {preco}')  # Exibe o nome e o preço no console
            produtos['titulo'].append(nome)  # Adiciona o nome ao dicionário
            produtos['preco'].append(preco)  # Adiciona o preço ao dicionário
        except Exception as e:
            print(f'Erro ao coletar dados: {e}')  # Mostra o erro caso não consiga coletar algum dado

    try:
        botao_proximo = WebDriverWait(executador, 10).until(
            ec.element_to_be_clickable((By.CLASS_NAME, 'nextLink'))
        )  # Espera até que o botão de próxima página esteja clicável

        if botao_proximo:  # Se o botão existir
            executador.execute_script('arguments[0].scrollIntoView();', botao_proximo)  
            # Faz scroll até o botão
            time.sleep(1)  
            # Aguarda um segundo
            executador.execute_script('arguments[0].click();', botao_proximo)  
            # Clica no botão usando JavaScript
            print(f'Indo para a página {pagina_atual}')  # Mostra que está indo para a próxima página
            pagina_atual += 1  # Incrementa o número da página atual
            time.sleep(5)  # Aguarda 5 segundos para a próxima página carregar
        else:
            print('Você chegou na última página!')  # Informa que não há mais páginas
            break  # Sai do loop
    except Exception as e:
        print('Erro ao tentar avançar para a próxima página:', e)  # Informa erro ao tentar clicar no botão
        break  # Sai do loop

executador.quit()  
# Fecha o navegador após o término do scraping

df = pd.DataFrame(produtos)  
# Cria um DataFrame com os dados coletados

df.to_excel('cadeiras.xlsx', index=False)  
# Salva os dados em um arquivo Excel chamado 'cadeiras.xlsx'

print(f'Arquivo "cadeiras" salvo com sucesso! ({len(df)} produtos capturados)')  
# Informa que o arquivo foi salvo com sucesso e mostra a quantidade de produtos
