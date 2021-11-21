#!/usr/bin/python3
################################## AUTOR #########################################
# Data: 21.11.2021                                                               #
# Author: Jefferson Ruiz                                                         #
# Email: jefferson.ruiz@outlook.com                                              #
# Repositorio: https://github.com/JeffersonARuiz/Zabbix_Grafana_AppleStore       #
# Descrição: Script que verifica/extrai as informações da página da Google Play  #
# Versão: 1.0                                                                    #
##################################################################################
import os
import sys
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver


#URL da loja Google Play.
URL_BASE = "https://play.google.com/store/apps/details?id="

#Exemplo de USO --> ./googleplay.py <id-do-app> <tipoVerificacao> 

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print("Necessário informar dois parametros para execução do Script:")
        print("1 - ID do App na Google Play Brasil.")
        print("2 - Tipo de verificação [ Nota | Versao | Avaliacoes | Debug ].")

        sys.exit(1)

    else: 

        try:
        
            #Salvando os parametros enviados nas variaveis 
            id_aplicacao = sys.argv[1]
            tipoVerificacao = sys.argv[2]

            #Formatando a URl completa para Google Play
            URL_FORMATADA = URL_BASE + id_aplicacao

            #Definindo as parametrizações dos componentes para utilização do Navegador (Chrome e/ou Firefox) 

            ####### $$$$$ PARA GOOGLE CHROME | DESCOMENTE AS LINHAS ABAIXO $$$$$ ########
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

            ####### $$$$$ PARA FIREFOX | DESCOMENTE AS LINHAS ABAIXO $$$$$ ########
            #from selenium.webdriver.firefox.options import Options
            #firefox_options = Options()
            #firefox_options.add_argument('--headless')
            #firefox_options.add_argument('--no-sandbox')
            #firefox_options.add_argument('--disable-dev-shm-usage')


            #Definindo parametros de resolução de tela, mesmo que não estejamos abrindo o browser/janela no script (visible = 0) e exibindo o display.
            display = Display(visible = 0, size = (1024, 768))
            display.start()

            ####### $$$$$ PARA FIREFOX | DESCOMENTE A LINHA ABAIXO $$$$$ ########
            #navegador = webdriver.Firefox(options=firefox_options)

            ####### $$$$$ PARA GOOGLE CHROME | DESCOMENTE A LINHA ABAIXO $$$$$ ########
            navegador = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options)

            #Fazendo get na URL final e salvando na variável response_html o retorno (page_source)
            navegador.get(URL_FORMATADA)
            response_html = navegador.page_source

            #Fazedo parse na resposta (response_html) através do BeautifulSoup e salvando na variavel "site".
            site = BeautifulSoup(response_html, 'html.parser')

            #Obtendo o nome do App conforme exibição na loja Google Play
            titulo_aplicacao = site.find('h1', class_='AHFaub').text.strip()


            ##### FUNÇÃO PARA VERIFICAR A NOTA DO APP
            def NotaApp():

                try:
                    #Obtendo a nova do App existente na Google Play
                    nota_app = site.find('div', class_='BHMmbe').text.strip().replace(',','.')

                    #retornando a Nota do App
                    return nota_app

                except:

                    nota_app = 0
                    return nota_app

            ##### FUNÇÃO PARA VERIFICAR A VERSÃO DO APP
            def VersaoApp():

                try:
                    #Localizando a estrutura de DIVs existentes na Google PLay para obter a versao do App
                    conteudo_div = site.find('div', class_='IxB2fe') # DIV Principal
                    elementos = conteudo_div.find_all('div', class_='hAyfc') #DIV filho para fazer o Loop 

                    #Fazendo Loop em todos os elementos do DIV Filho para localizar o DIV com a versão, pois todos possuem a mesma classe e ID.
                    for elemento in elementos:
                        #Pesquisando cada div interno dos elementos (div Filho) para localizar o titulo Versão atual ou Current Version (ingles)
                        item = elemento.find('div', class_='BgcNfc').text.strip()

                        #print(item + " => " + elemento.find('span', class_='htlgb').text.strip() ) #Debug Print
                        
                        #Se um dos divs for localizado com o titulo "Versão atual" ou "Current Version", executa o comando find no div interno para pegar a versao do App. 
                        if item == 'Current Version' or item == 'Versão atual':
                            versao = elemento.find('span', class_='htlgb').text.strip()
                            return versao
                    
                except:
                    versao = "0.0"
                    return versao

            ##### FUNÇÃO PARA VERIFICAR A QUANTIDADE DE AVALIACOES DO APP
            def AvaliacoesApp():

                try:
                    #Coletando a quantidade de avaliações existentes na Google Play.
                    qtdAvaliacoes = site.find('span', class_='AYi5wd TBRnV').text.strip()
                    avaliacoes = qtdAvaliacoes.replace('.','').replace(',','').strip()
                    
                    return avaliacoes

                except:
                    
                    qtdAvaliacoes = "0"
                    return qtdAvaliacoes


            #Execucao do Código para chamadas do tipo = Avaliacoes
            if tipoVerificacao == 'Avaliacoes':
                
                #Chamando a função que verifica a quantidade de avaliações do App
                quantidade = AvaliacoesApp()
                #imprimindo a Qtd. Avaliacoes do App.
                print(int(quantidade))
                

            #Execucao do Código para chamadas do tipo = Nota
            if tipoVerificacao == 'Nota':
                #Chamando a função que verifica a nota do App
                nota = NotaApp()
                #imprimindo a Nota do App.
                print(float(nota))
                

            #Execucao do Código para chamadas do tipo = Versao
            if tipoVerificacao == 'Versao':
                #Chamando a função que verifica a versão do App
                versao = VersaoApp()
                #imprimindo a Versao do App.
                print(versao)
                

            #Execucao do Código para chamadas do tipo = Debug
            if tipoVerificacao == 'Debug':
                
                nota = NotaApp()
                versao = VersaoApp()
                quantidade = AvaliacoesApp()

                print("App: " +  titulo_aplicacao + " | Versao: " + versao + " | Nota App Store: " + str(nota) + " | Qtd. Avaliações: " + str(quantidade) + "")

            #Fechando o Browser e o Display para liberação de recursos e encerramento dos processos no S.O.
            navegador.close()
            navegador.quit()
            display.stop()  
            

        except:

            #Fechando o Browser e o Display para liberação de recursos e encerramento dos processos no S.O.
            navegador.close()
            navegador.quit()
            display.stop()
            
            #Erros para exceção do Script durante a execução.
            print("Ocorreu um erro ao processar o Script")