import models.gt

from time import sleep

"""
import PySimpleGUI as sg

def criar_janela_inicial():
    sg.theme('DarkBlue4')
    linha = [
        [sg.Checkbox(''), sg.Input('')],
    ]
    layout =  [
        [sg.Frame('Tarefas',  layout = linha, key='container')],
        [sg.Button('Nova Tarefa'),sg.Button('Resetar')],
    ]

    return sg.Window('Todo List', layout=layout, finalize=True)

janela =  criar_janela_inicial()

while True:
    event, values = janela.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Nova Tarefa':
        janela.extend_layout(janela['container'],[[sg.Checkbox(''), sg.Input('')]],)
    elif event ==  'Resetar':
        janela.close()
        janela = criar_janela_inicial()"""


import customtkinter as ctk

#configurar a aparência

ctk.set_appearance_mode('dark')

#Criação das funções de funcionalidades
def validar_login():
    usuario = campo_usuario.get()
    senha = campo_senha.get()

    if usuario == 'bruno' and senha == '123456':
        resultado_login.configure(text='Login feito com sucesso', text_color='green')
    else:
        resultado_login.configure(text='Login Incorreto!', text_color='red')

#criação de tela inicial

app = ctk.CTk()
app.title('Sistema de Login')
app.geometry('350x350')

#criação de campos

#Label - Usuário
label_usuario = ctk.CTkLabel(app, text='Usuário')
label_usuario.pack(pady=10)

#entry - Campo de usuário
campo_usuario = ctk.CTkEntry(app, placeholder_text='Digite seu usuário')
campo_usuario.pack(pady=10)

#Label - Senha
label_senha = ctk.CTkLabel(app, text='Senha', )
label_senha.pack()

#entry - Campo de usuário
campo_senha = ctk.CTkEntry(app, placeholder_text='Digite sua senha', show='*')
campo_senha.pack(pady=10)
#Button
botao_login = ctk.CTkButton(app, text='Login', command=validar_login)
botao_login.pack()

#campo feedback de login
resultado_login = ctk.CTkLabel(app, text='')
resultado_login.pack(pady=10)




#iniciar a aplicação
app.mainloop()