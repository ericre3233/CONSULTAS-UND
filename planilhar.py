import sys
from typing import Self
from botcity.core import DesktopBot

# Verificação do módulo select usando a janela de erro existente
try:
    import select
except ImportError:
    bot = DesktopBot()
    bot.show_error_window()
    sys.exit(1)
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
import tkinter as tk
from tkinter import messagebox


link_file = "link.txt"  # Nome do arquivo para armazenar o link
config_file = "config.txt"
contagem = [str(i) for i in range(1, 10001, 1)]  # Lista de 1 a 10000

def save_link(link):
    with open(link_file, "w") as file:
        file.write(link)

def load_link():
    if os.path.exists(link_file):
        with open(link_file, "r") as file:
            return file.read().strip()
    return ""


def save_config(config):
    try:
        with open(config_file, "w") as file:
            for key, value in config.items():
                file.write(f"{key}={value}\n")
        print("Configurações salvas com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar configurações: {e}")


def load_config():
    config = {
        "apos_colar_cpf": 1,
        "apos_primeiro_esc": 1,
        "apos_segundo_esc": 0,
        "apos_pressionar_down": 1,
        "apos_pressionar_enter_pesquisacpf": 1,
        "apos_clicar_processo": 1,
        "apos_clicar_enviar": 0
    }
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as file:
                for line in file:
                    if "=" in line:
                        key, value = line.strip().split("=")
                        config[key] = int(value)
            print("Configurações carregadas com sucesso.")
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
    return config

link_salvo = load_link()  # Carregar o link ao iniciar o bot
config = load_config()

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


def encerrar_programa(janela):
    print("Encerrando o programa...")
    release_keys()
    janela.destroy()
    os._exit(0)


def parar():
    while True:
        if keyboard.is_pressed('r'):
            release_keys()
            python = sys.executable
            os.execl(python, python, *sys.argv)

class Bot(DesktopBot):
    def action(self, execution=None):
        global link_salvo, config


        def abrir_configuracoes():
            # Verificar se a janela de configurações já está aberta
            if hasattr(abrir_configuracoes, "janela_config") and abrir_configuracoes.janela_config.winfo_exists():
                abrir_configuracoes.janela_config.lift()  # Traz a janela existente para frente
                return

            # Criar a janela de configurações
            abrir_configuracoes.janela_config = ttk.Toplevel()
            janela_config = abrir_configuracoes.janela_config
            janela_config.title("Configurações")
            janela_config.configure(bg="white") 

            # Obter a posição da janela principal
            x_principal = app.winfo_x()
            y_principal = app.winfo_y()

            # Definir a posição e o tamanho da janela de configurações
            largura = 400
            altura = 400  # Aumentar a altura para 400 pixels
            x_config = x_principal + 50  # 50 pixels à direita da janela principal
            y_config = y_principal + 50  # 50 pixels abaixo da janela principal
            janela_config.geometry(f"{largura}x{altura}+{x_config}+{y_config}")

            # Variáveis para armazenar os valores padrão
            apos_colar_cpf_var = tk.StringVar(value=str(config["apos_colar_cpf"]))
            apos_primeiro_esc_var = tk.StringVar(value=str(config["apos_primeiro_esc"]))
            apos_segundo_esc_var = tk.StringVar(value=str(config["apos_segundo_esc"]))
            apos_pressionar_down_var = tk.StringVar(value=str(config["apos_pressionar_down"]))
            apos_pressionar_enter_pesquisacpf_var = tk.StringVar(value=str(config["apos_pressionar_enter_pesquisacpf"]))
            apos_clicar_processo_var = tk.StringVar(value=str(config["apos_clicar_processo"]))
            apos_clicar_enviar_var = tk.StringVar(value=str(config["apos_clicar_enviar"]))

            # Valores predefinidos para os Combobox
            valores_tempo = [str(i) for i in range(0, 61)]  # Valores de 0 a 60 segundos

            # Configurar layout com grid
            janela_config.grid_rowconfigure(0, weight=1)
            janela_config.grid_rowconfigure(6, weight=1)
            janela_config.grid_columnconfigure(0, weight=1)
            janela_config.grid_columnconfigure(2, weight=1)

            ttk.Label(janela_config, text="Configurações - Tempo(segundos)", font=("Helvetica", 16), background="white", foreground="black").grid(row=0, column=0, columnspan=2, pady=10)

            # Ajustar os campos e botões na janela de configurações
            ttk.Label(janela_config, text="Após colar cpf, em notificações:", background="white", foreground="black").grid(row=1, column=0, sticky="e", padx=10, pady=5)
            ttk.Combobox(janela_config, textvariable=apos_colar_cpf_var, values=valores_tempo).grid(row=1, column=1, sticky="w", padx=10, pady=5)

            ttk.Label(janela_config, text="Após 1º esc, para sair de notificações:", background="white", foreground="black").grid(row=2, column=0, sticky="e", padx=10, pady=5)
            ttk.Combobox(janela_config, textvariable=apos_primeiro_esc_var, values=valores_tempo).grid(row=2, column=1, sticky="w", padx=10, pady=5)

            ttk.Label(janela_config, text="Após 2º esc, para sair de notificações:", background="white", foreground="black").grid(row=3, column=0, sticky="e", padx=10, pady=5)
            ttk.Combobox(janela_config, textvariable=apos_segundo_esc_var, values=valores_tempo).grid(row=3, column=1, sticky="w", padx=10, pady=5)

            ttk.Label(janela_config, text="Após seta para baixo, prox cpf:", background="white", foreground="black").grid(row=4, column=0, sticky="e", padx=10, pady=5)
            ttk.Combobox(janela_config, textvariable=apos_pressionar_down_var, values=valores_tempo).grid(row=4, column=1, sticky="w", padx=10, pady=5)

            ttk.Label(janela_config, text="Após enter, na pesquisa do cpf:", background="white", foreground="black").grid(row=5, column=0, sticky="e", padx=10, pady=5)
            ttk.Combobox(janela_config, textvariable=apos_pressionar_enter_pesquisacpf_var, values=valores_tempo).grid(row=5, column=1, sticky="w", padx=10, pady=5)

            ttk.Label(janela_config, text="Após clicar no número do processo:", background="white", foreground="black").grid(row=6, column=0, sticky="e", padx=10, pady=5)
            ttk.Combobox(janela_config, textvariable=apos_clicar_processo_var, values=valores_tempo).grid(row=6, column=1, sticky="w", padx=10, pady=5)

            ttk.Label(janela_config, text="Após clicar em enviar processo:", background="white", foreground="black").grid(row=7, column=0, sticky="e", padx=10, pady=5)
            ttk.Combobox(janela_config, textvariable=apos_clicar_enviar_var, values=valores_tempo).grid(row=7, column=1, sticky="w", padx=10, pady=5)

            # Função para salvar as configurações
            def salvar_config():
                try:
                    config["apos_colar_cpf"] = int(apos_colar_cpf_var.get())
                    config["apos_primeiro_esc"] = int(apos_primeiro_esc_var.get())
                    config["apos_segundo_esc"] = int(apos_segundo_esc_var.get())
                    config["apos_pressionar_down"] = int(apos_pressionar_down_var.get())
                    config["apos_pressionar_enter_pesquisacpf"] = int(apos_pressionar_enter_pesquisacpf_var.get())
                    config["apos_clicar_processo"] = int(apos_clicar_processo_var.get())
                    config["apos_clicar_enviar"] = int(apos_clicar_enviar_var.get())


                    save_config(config)
                    messagebox.showinfo("Configurações", "Configurações salvas com sucesso!", parent=janela_config)
                    janela_config.destroy()
                except ValueError:
                    messagebox.showerror("Erro", "Por favor, insira valores válidos.", parent=janela_config)

            # Botões "Salvar" e "Cancelar" movidos para linhas mais abaixo
            ttk.Button(
                janela_config,
                text="Salvar",
                bootstyle=SUCCESS,
                command=salvar_config
            ).grid(row=8, column=0, pady=20, padx=10, sticky="e")

            ttk.Button(
                janela_config,
                text="Cancelar",
                bootstyle=DANGER,
                command=janela_config.destroy
            ).grid(row=8, column=1, pady=20, padx=10, sticky="w")









        try:
            # Criar a janela principal
            app = ttk.Window(themename="darkly")  # Escolha um tema moderno
            app.title("INSERI AS CONSULTAS E ENVIA PARA UNDIDADE")
            app.geometry("550x500")  # Defina o tamanho da janela
            app.configure(bg="white")  # Definir o fundo branco



            
            menu_bar = ttk.Menu(app)
            menu_inicio = ttk.Menu(menu_bar, tearoff=0)
            menu_inicio.add_command(label="Sair", command=lambda: encerrar_programa(app))
            menu_bar.add_cascade(label="Início", menu=menu_inicio)

            menu_config = ttk.Menu(menu_bar, tearoff=0)
            menu_config.add_command(label="Configurações", command=abrir_configuracoes)
            menu_bar.add_cascade(label="Configurações", menu=menu_config)

            app.config(menu=menu_bar)

            # Layout principal com grid
            app.grid_rowconfigure(0, weight=1)
            app.grid_rowconfigure(6, weight=1)
            app.grid_columnconfigure(0, weight=1)
            app.grid_columnconfigure(3, weight=1)


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
        global link_salvo, config
        save_link(link)
        threading.Thread(target=interromper).start()
        threading.Thread(target=parar).start()
        webbrowser.open(link)
        inserirconsulta(0, int(quantidade), bot=self, self=self, config=config)

    def inserir_consultas_dirat(self, link, quantidade):
        save_link(link)
        threading.Thread(target=interromper).start()
        threading.Thread(target=parar).start()
        webbrowser.open(link)
        inserirconsultadirat(0, int(quantidade), bot=self, self=self, config=config)

    def inserir_consultas_coord(self, link, quantidade):
        save_link(link)
        threading.Thread(target=interromper).start()
        threading.Thread(target=parar).start()
        webbrowser.open(link)
        inserirconsultacoord(0, int(quantidade), bot=self, self=self, config=config)

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