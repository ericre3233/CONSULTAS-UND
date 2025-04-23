import threading
import time
from botcity.core import DesktopBot
import keyboard
from datetime import date

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

def anotacao(contador, cont, bot: DesktopBot, self: DesktopBot, executation=None):
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
            # Copiar o conteúdo da célula à esquerda
            bot.type_keys(["left"])
            bot.type_keys(["ctrl", "c"])
            #bot.type_keys(["right"])
            #bot.type_keys(["down"] * 1)
            #bot.type_keys(["ctrl", "tab"])  
            #inserir2(contador, cont, bot, self)
            inserir(contador, cont, bot, self)
                

   
        bot.type_keys(["down"])
        anotacao(contador, cont, bot=self, self=self)
        
        

def inserir(contador, cont, bot: DesktopBot, self: DesktopBot, executation=None):
      


        #bot.type_keys(["ctrl", "tab"])
        bot.type_keys(["ctrl", "x"])
        bot.type_keys(["up"] * 1)
        bot.type_keys(["shift", "f2"])
        #bot.type_keys(["espace"])
        bot.type_keys(["ctrl", "v"])
        bot.type_keys(["espace"])
        #bot.type_keys(["escape"])
        bot.type_keys(["escape"])
        bot.type_keys(["down"] * 1)
        bot.type_keys(["ctrl", "shift", "-"])
        bot.type_keys(["down"] * 2)
        bot.type_keys(["enter"])
        bot.type_keys(["right"] * 1)
        


        contador = contador + 1
        bot.type_keys(["ctrl", "tab"])
        anotacao(contador, cont, bot=self, self=self)

