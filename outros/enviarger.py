import time
from botcity.core import DesktopBot


def enviarger(contador, cont, bot: DesktopBot, self: DesktopBot, executation=None):

    while contador < cont:
        self.wait(1000)
        bot.type_keys(["ctrl", "tab"])
        bot.type_keys(["ctrl", "c"])
        bot.type_keys(["ctrl", "tab"])

        if not bot.find("pesq", matching=0.85, waiting_time=1000):
            self.not_found("pesq")
        
        bot.click()
        bot.type_keys(["ctrl", "v"])
        bot.type_keys(["enter"])
        self.wait(1000)

        imagem = ["enviar"]
        for img in imagem:
            try:
                if not bot.find(img, matching=0.85, waiting_time=1000):
                    self.not_found(img)
                bot.click()
                break  # Se encontrou a imagem, sai do loop
            except:
                continue   

        # Digitar "GERAP"
        bot.type_keys("GERAP")
        self.wait(2000)
        bot.type_down() 
        bot.type_down() 
        self.enter()
        for _ in range(3):  # Altere o número conforme necessário
           bot.type_keys(["shift", "tab"])
        self.enter()
        bot.type_keys(["ctrl", "tab"])
        bot.type_down() 
        bot.type_keys(["ctrl", "tab"])


        contador += 1
