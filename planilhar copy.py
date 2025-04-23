from typing import Self
from botcity.core import DesktopBot
from inserirconsulta import inserirconsulta
from inserirconsultadirat import inserirconsultadirat
from inserirconsultacoord import inserirconsultacoord
import webbrowser
import sys
import os
import keyboard
import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

link_file = "link.txt"  # Nome do arquivo para armazenar o link

contagem = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
    "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "35", "40", "45", "50", "100", "150", "200", "250",
    "300", "350"
]

def save_link(link):
    with open(link_file, "w") as file:
        file.write(link)

def load_link():
    if os.path.exists(link_file):
        with open(link_file, "r") as file:
            return file.read().strip()
    return ""

link_salvo = load_link()  # Carregar o link ao iniciar o bot

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def release_keys():
    if keyboard.is_pressed('ctrl'):
        keyboard.release('ctrl')
    if keyboard.is_pressed('shift'):
        keyboard.release('shift')

def interromper():
    while True:
        if keyboard.is_pressed('e'):
            release_keys()
            os._exit(0)

def parar():
    while True:
        if keyboard.is_pressed('r'):
            release_keys()
            python = sys.executable
            os.execl(python, python, *sys.argv)

class Bot(DesktopBot):
    def action(self, execution=None):
        global link_salvo  # Usar a variável global
        try:
            # Criar a janela principal
            app = ttk.Window(themename="darkly")  # Escolha um tema moderno
            app.title("INSERI AS CONSULTAS E ENVIA PARA UNDIDADE")
            app.geometry("550x500")  # Defina o tamanho da janela
            app.configure(bg="white")  # Definir o fundo branco

            # Criar estilos personalizados para os campos
            style = ttk.Style()
            style.configure("Custom.TEntry", fieldbackground="#f0f0f0", foreground="black")
            style.configure("Custom.TCombobox", fieldbackground="#f0f0f0", foreground="black")
            style.map("Custom.TCombobox", fieldbackground=[("readonly", "#f0f0f0"), ("focus", "#e6e6e6")])

            # Layout
            ttk.Label(app, text="Link:", anchor=E, background="white", foreground="black").grid(row=0, column=0, padx=10, pady=10, sticky=E)
            link_entry = ttk.Entry(app, width=50, style="Custom.TEntry")
            link_entry.insert(0, link_salvo)
            link_entry.grid(row=0, column=1, padx=10, pady=10)

            ttk.Label(app, text="Quantidade de processos enviar:", anchor=E, background="white", foreground="black").grid(row=1, column=0, padx=10, pady=10, sticky=E)
            quantidade_combo = ttk.Combobox(app, values=contagem, width=10, style="Custom.TCombobox")
            quantidade_combo.set(contagem[0])
            quantidade_combo.grid(row=1, column=1, padx=10, pady=10, sticky=W)

            ttk.Label(app, text="Para interromper e voltar ao menu principal, pressione 'r'.", anchor=CENTER, background="white", foreground="red").grid(row=2, column=0, columnspan=2, padx=10, pady=10)
            ttk.Label(app, text="Para fechar, pressione 'e'.", anchor=CENTER, background="white", foreground="red").grid(row=3, column=0, columnspan=2, padx=10, pady=10)

            ttk.Label(app, text="A opção abaixo insere as consultas e envia os processos para a COORD ou GERAP:", anchor=CENTER, wraplength=500, background="white", foreground="black").grid(row=4, column=0, columnspan=2, padx=10, pady=10)
            ttk.Button(app, text="INSERIR CONSULTAS", bootstyle=PRIMARY, command=lambda: self.inserir_consultas(link_entry.get(), quantidade_combo.get())).grid(row=5, column=0, columnspan=2, pady=10)

            ttk.Label(app, text="A opção abaixo insere as consultas e envia os processos apenas para a DIRAT:", anchor=CENTER, wraplength=500, background="white", foreground="black").grid(row=6, column=0, columnspan=2, padx=10, pady=10)
            ttk.Button(app, text="INSERIR CONSULTAS / ENVIAR DIRAT", bootstyle=SUCCESS, command=lambda: self.inserir_consultas_dirat(link_entry.get(), quantidade_combo.get())).grid(row=7, column=0, columnspan=2, pady=10)

            ttk.Label(app, text="A opção abaixo insere as consultas e envia os processos apenas para COORD, mesmo que haja divergência de endereço:", anchor=CENTER, wraplength=500, background="white", foreground="black").grid(row=8, column=0, columnspan=2, padx=10, pady=10)
            ttk.Button(app, text="INSERIR CONSULTAS / ENVIAR COORD", bootstyle=WARNING, command=lambda: self.inserir_consultas_coord(link_entry.get(), quantidade_combo.get())).grid(row=9, column=0, columnspan=2, pady=10)

            # Iniciar o loop principal
            app.mainloop()

        except Exception as e:
            self.show_error_window()

    def inserir_consultas(self, link, quantidade):
        save_link(link)
        threading.Thread(target=interromper).start()
        threading.Thread(target=parar).start()
        webbrowser.open(link)
        inserirconsulta(0, int(quantidade), bot=self, self=self)

    def inserir_consultas_dirat(self, link, quantidade):
        save_link(link)
        threading.Thread(target=interromper).start()
        threading.Thread(target=parar).start()
        webbrowser.open(link)
        inserirconsultadirat(0, int(quantidade), bot=self, self=self)

    def inserir_consultas_coord(self, link, quantidade):
        save_link(link)
        threading.Thread(target=interromper).start()
        threading.Thread(target=parar).start()
        webbrowser.open(link)
        inserirconsultacoord(0, int(quantidade), bot=self, self=self)

    def show_error_window(self):
        error_app = ttk.Window(themename="darkly")
        error_app.title("ERRO")
        error_app.geometry("400x300")

        ttk.Label(error_app, text="OCORREU UM ERRO!!", anchor=CENTER).pack(pady=10)
        ttk.Label(error_app, text="GENTILEZA REINICIAR O APLICATIVO !!!", anchor=CENTER).pack(pady=10)
        ttk.Label(error_app, text="COPIAR E COLAR LINK - FECHAR NAVEGADOR", anchor=CENTER).pack(pady=10)
        ttk.Label(error_app, text="EM SEGUIDA CLICAR NO BOTÃO CORRESPONDENTE AO PROCESSO!!", anchor=CENTER).pack(pady=10)
        ttk.Button(error_app, text="REINICIAR", bootstyle=DANGER, command=restart_program).pack(pady=20)

        error_app.mainloop()

if __name__ == '__main__':
    Bot.main()