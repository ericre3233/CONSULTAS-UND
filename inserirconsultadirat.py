
import threading
import time
from botcity.core import DesktopBot
import keyboard
from datetime import date
import os

def carregar_config():
    """Carrega as configurações do arquivo config.txt"""
    config = {
        "apos_colar_cpf": 1,
        "apos_primeiro_esc": 1,
        "apos_segundo_esc": 0,
        "apos_pressionar_down": 1,
        "apos_pressionar_enter_pesquisacpf": 1,
        "apos_clicar_processo": 1,
        "apos_clicar_enviar": 0
    }
    
    try:
        with open('config.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = int(value.strip())
    except Exception as e:
        print(f"Erro ao carregar config.txt: {e}. Usando valores padrão.")
    
    return config

data_atual = date.today()
data = data_atual.strftime("%d/%m/%Y")

execucao_permitida = False

def monitorar_tecla(contador, cont, bot: DesktopBot, self: DesktopBot):
    while (contador < cont):   
        global execucao_permitida
        while True:
            if keyboard.is_pressed('t'):    
                execucao_permitida = True
                time.sleep(0.5)  # Delay para evitar múltiplas chamadas rápidas

def inserirconsultadirat(contador, cont, bot: DesktopBot, self: DesktopBot, contador_celulas_vazias=0, executation=None, config=None):
    if config is None:
        config = carregar_config()
    global execucao_permitida

    while (contador < cont):
        self.wait(1000)
        bot.type_keys(["ctrl", "tab"])

        # Verificar se a célula está vazia antes de copiar
        bot.type_keys(["ctrl", "c"])
        self.wait(500)
        bot.type_keys(["ctrl", "v"])
        self.wait(500)
        copied_text = self.get_clipboard()
        
        if copied_text.strip() == "":
        #if copied_text.strip() == "":
            # Incrementar o contador de células vazias
            contador_celulas_vazias += 1
            print(f"Células vazias encontradas: {contador_celulas_vazias}")

            # Copiar o conteúdo da célula à esquerda
            inserir3(contador, cont, bot, self, contador_celulas_vazias)
        else:
            if contador_celulas_vazias > 0:
                print(f"Quantidade de células vazias encontradas: {contador_celulas_vazias}")
                try:
                    print(f"Executando bot.type_keys(['up'] * (contador_celulas_vazias + 1))")
                    bot.type_keys(["up"] * (contador_celulas_vazias+1))
                    bot.type_keys(["right"] * 3)
                    print(f"Comando bot.type_keys executado com {contador_celulas_vazias + 1} teclas 'up'.")

                    self.paste("DIRAT")
                    bot.type_keys(["right"] * 1)                    
                    self.paste("OK")
                    bot.type_keys(["down"] * 1) 
                    bot.type_keys(["left"] * 5) 

                    bot.type_keys(["ctrl", "tab"])

                    self.wait(1000)

                    if not bot.find("processo", matching=0.97, waiting_time=10000):
                        self.not_found("processo")
                    bot.click()

                    time.sleep(config["apos_clicar_processo"])

                    if not bot.find("enviar", matching=0.97, waiting_time=10000):
                        self.not_found("enviar")
                    bot.click()

                    time.sleep(config["apos_clicar_enviar"])
                    self.paste("DIRAT")
                    self.wait(1000)
                    bot.type_keys(["down"])
                    bot.type_keys(["enter"])
                    bot.type_keys(["shift", "tab", "shift", "tab", "shift", "tab"])
                    bot.type_keys(["enter"])
                    bot.type_keys(["escape"])

                   

                    #if not bot.find("enviar", matching=0.97, waiting_time=10000):
                    #    self.not_found("enviar")
                    #bot.click()

                    bot.type_keys(["ctrl", "tab"])
                    #bot.type_keys(["left"] * 5)
                    #bot.type_keys(["down"] * 1)

                    print(f"Quantidade de células vazias: {contador_celulas_vazias}")
                    while contador_celulas_vazias > 0:                 
                    
                        bot.type_keys(["ctrl", "x"])
                        bot.type_keys(["up"] * 1)
                        bot.type_keys(["shift", "f2"])
                        bot.type_keys(["space"])
                        bot.type_keys(["ctrl", "v"])
                        time.sleep(config["apos_colar_cpf"])
                        bot.type_keys(["escape"])
                        time.sleep(config["apos_primeiro_esc"])
                        bot.type_keys(["escape"])
                        time.sleep(config["apos_segundo_esc"])
                        bot.type_keys(["down"] * 1)
                        time.sleep(config["apos_pressionar_down"])
                        bot.type_keys(["ctrl", "shift", "-"])
                        self.wait(1000)
                        bot.type_keys(["down"] * 2)
                        bot.type_keys(["enter"])
                        self.wait(1000)
                        contador_celulas_vazias -= 1
                
                    #bot.type_keys(["right"] * 1)
                    bot.type_keys(["right"] * 1)
                    bot.type_keys(["ctrl", "c"])
                    contador_celulas_vazias == 0

                        #contador_celulas_vazias -= 1



                except Exception as e:
                    print(f"Erro ao executar bot.type_keys: {e}")
                
   # Só executar os comandos seguintes se o contador de células vazias estiver em zero
        if contador_celulas_vazias == 0:
            bot.type_keys(["ctrl", "tab"])
            if not bot.find("pesq", matching=0.85, waiting_time=1000):
                self.not_found("pesq")
            bot.click()
            bot.type_keys(["ctrl", "v"])
            bot.type_keys(["enter"])
            self.wait(1000)
            bot.type_keys(["ctrl", "tab"])
            # Verificar se a célula abaixo não está vazia
            bot.type_keys(["down"])
            bot.type_keys(["ctrl", "c"])
            self.wait(500)
            copied_text_baixo = self.get_clipboard()
            bot.type_keys(["up"])  # Voltar para a célula original

            if copied_text_baixo.strip() == "":
                print("Célula abaixo do processo está vazia. Chamando a função inserir.")
                bot.type_keys(["ctrl", "tab"])
                inserir(contador, cont, bot=self, self=self, contador_celulas_vazias=contador_celulas_vazias)
            else:
                print("Célula abaixo não está vazia. Chamando a função inserir2.")
                bot.type_keys(["ctrl", "tab"])
                inserir2(contador, cont, bot=self, self=self, contador_celulas_vazias=contador_celulas_vazias)
                
            

def inserir(contador, cont, bot: DesktopBot, self: DesktopBot, contador_celulas_vazias=0, executation=None, config=None):
    if config is None:
        config = carregar_config()
    
    if not bot.find("novo", matching=0.97, waiting_time=10000):
        self.not_found("novo")
    bot.click()
    self.wait(1000)
    self.type_down()
    self.enter()
    self.wait(1000)

    if not bot.find("seta", matching=0.97, waiting_time=10000):
        self.not_found("seta")
    bot.click()

    self.kb_type("Consulta")
    self.enter()

    if not bot.find("data", matching=0.97, waiting_time=10000):
        self.not_found("data")
    bot.click_relative(24, 34)
    self.paste(data)

    if not bot.find("nato", matching=0.97, waiting_time=10000):
        self.not_found("nato")
    self.click()

    bot.type_keys(["ctrl", "tab"])
    bot.type_keys(["left"] * 1)
    bot.type_keys(["ctrl", "c"])
    bot.type_keys(["ctrl", "tab"])

    bot.type_keys(["shift", "tab", "shift", "tab", "shift", "tab", "shift", "tab"])
    bot.type_keys(["left"] * 1)
    bot.type_keys(["tab"])
    self.enter()

    if not bot.find("downloads", matching=0.97, waiting_time=10000):
        self.not_found("downloads")
    self.click()

    bot.type_keys(["shift", "tab", "shift", "tab"])
    bot.type_keys(["ctrl", "v"])
    bot.type_keys(["enter"])
    time.sleep(config["apos_pressionar_enter_pesquisacpf"])
    bot.type_keys(["tab"])
    bot.type_keys(["down"] * 1)
    bot.type_keys(["space"])
    bot.type_keys(["enter"])
    self.wait(1000)
    bot.type_keys(["tab"])
    bot.type_keys(["enter"])
    self.wait(1000)

    bot.type_keys(["ctrl", "tab"])


    bot.type_keys(["right"] * 1)
    bot.type_keys(["down"] * 1)
    bot.type_keys(["ctrl", "tab"])

    contador = contador + 1
    inserirconsultadirat(contador, cont, bot=self, self=self, contador_celulas_vazias=contador_celulas_vazias)






def inserir2(contador, cont, bot: DesktopBot, self: DesktopBot, contador_celulas_vazias=0, executation=None, config=None):
    if config is None:
        config = carregar_config()
    if not bot.find("novo", matching=0.97, waiting_time=10000):
        self.not_found("novo")
    bot.click()
    self.wait(1000)
    self.type_down()
    self.enter()
    self.wait(1000)

    if not bot.find("seta", matching=0.97, waiting_time=10000):
        self.not_found("seta")
    bot.click()

    self.kb_type("Consulta")
    self.enter()

    if not bot.find("data", matching=0.97, waiting_time=10000):
        self.not_found("data")
    bot.click_relative(24, 34)
    self.paste(data)

    if not bot.find("nato", matching=0.97, waiting_time=10000):
        self.not_found("nato")
    self.click()

    bot.type_keys(["ctrl", "tab"])
    bot.type_keys(["left"] * 1)
    bot.type_keys(["ctrl", "c"])
    bot.type_keys(["ctrl", "tab"])

    bot.type_keys(["shift", "tab", "shift", "tab", "shift", "tab", "shift", "tab"])
    bot.type_keys(["left"] * 1)
    bot.type_keys(["tab"])
    self.enter()

    if not bot.find("downloads", matching=0.97, waiting_time=10000):
        self.not_found("downloads")
    self.click()

    bot.type_keys(["shift", "tab", "shift", "tab"])
    bot.type_keys(["ctrl", "v"])
    bot.type_keys(["enter"])
    time.sleep(config["apos_pressionar_enter_pesquisacpf"])
    bot.type_keys(["tab"])
    bot.type_keys(["down"] * 1)
    bot.type_keys(["space"])
    bot.type_keys(["enter"])
    self.wait(1000)
    bot.type_keys(["tab"])
    bot.type_keys(["enter"])
    self.wait(1000)



    bot.type_keys(["ctrl", "tab"])
    bot.type_keys(["right"] * 4)
    self.paste("DIRAT")
    bot.type_keys(["right"] * 1)                    
    self.paste("OK")
    bot.type_keys(["down"] * 1) 
    bot.type_keys(["left"] * 4) 

    bot.type_keys(["ctrl", "tab"])

    
    if not bot.find("processo", matching=0.97, waiting_time=10000):
        self.not_found("processo")
    bot.click()

    time.sleep(config["apos_clicar_processo"])  

    if not bot.find("enviar", matching=0.97, waiting_time=10000):
        self.not_found("enviar")
    bot.click()

    time.sleep(config["apos_clicar_enviar"])     
    self.paste("DIRAT")
    self.wait(1000)
    bot.type_keys(["down"])
    bot.type_keys(["enter"])
    bot.type_keys(["shift", "tab", "shift", "tab", "shift", "tab"])
    bot.type_keys(["enter"])
    bot.type_keys(["escape"])


    
    #bot.type_keys(["ctrl", "tab"])
    
    #bot.type_keys(["right"] * 1)
    #bot.type_keys(["down"] * 1)
    #bot.type_keys(["ctrl", "tab"])


    contador = contador + 1
    inserirconsultadirat(contador, cont, bot=self, self=self, contador_celulas_vazias=contador_celulas_vazias)


def inserir3(contador, cont, bot: DesktopBot, self: DesktopBot, contador_celulas_vazias=0, executation=None, config=None):
    if config is None:
        config = carregar_config()

    bot.type_keys(["ctrl", "tab"])
    if not bot.find("novo", matching=0.97, waiting_time=10000):
        self.not_found("novo")
    bot.click()
    self.wait(1000)
    self.type_down()
    self.enter()
    self.wait(1000)

    if not bot.find("seta", matching=0.97, waiting_time=10000):
        self.not_found("seta")
    bot.click()

    self.kb_type("Consulta")
    self.enter()

    if not bot.find("data", matching=0.97, waiting_time=10000):
        self.not_found("data")
    bot.click_relative(24, 34)
    self.paste(data)

    if not bot.find("nato", matching=0.97, waiting_time=10000):
        self.not_found("nato")
    self.click()

    bot.type_keys(["ctrl", "tab"])
    bot.type_keys(["left"] * 1)
    bot.type_keys(["ctrl", "c"])
    bot.type_keys(["ctrl", "tab"])

    bot.type_keys(["shift", "tab", "shift", "tab", "shift", "tab", "shift", "tab"])
    bot.type_keys(["left"] * 1)
    bot.type_keys(["tab"])
    self.enter()



    if not bot.find("downloads", matching=0.97, waiting_time=10000):
        self.not_found("downloads")
    self.click()

    bot.type_keys(["shift", "tab", "shift", "tab"])
    bot.type_keys(["ctrl", "v"])
    bot.type_keys(["enter"])
    time.sleep(config["apos_pressionar_enter_pesquisacpf"])
    bot.type_keys(["tab"])
    bot.type_keys(["down"] * 1)
    bot.type_keys(["space"])
    bot.type_keys(["enter"])
    self.wait(1000)
    bot.type_keys(["tab"])
    bot.type_keys(["enter"])
    self.wait(1000)


    bot.type_keys(["ctrl", "tab"])


    bot.type_keys(["right"] * 1)
    bot.type_keys(["down"] * 1)
    bot.type_keys(["ctrl", "tab"])

    contador = contador + 1
    inserirconsultadirat(contador, cont, bot=self, self=self, contador_celulas_vazias=contador_celulas_vazias)