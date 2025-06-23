from models.gt import pega_dados

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

class Login(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Sistem de Login')
        self.geometry('350x350')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=0)

        self.label = ctk.CTkLabel(self, text="Faça seu Login", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, pady=20)

        self.usuario_entry = ctk.CTkEntry(self, placeholder_text="Usuário")
        self.usuario_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.senha_entry = ctk.CTkEntry(self, placeholder_text="Senha", show="*")
        self.senha_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.login = ctk.CTkButton(self, text="Entrar", command=self.validar_login)
        self.login.grid(row=3, column=0, padx=20, pady=10)

        self.status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.status_label.grid(row=4, column=0, pady=5)

    def validar_login(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()

        for _, v in enumerate(pega_dados()):
            if usuario == v[1] and senha == v[2]:
                self.status_label.configure(text='Login feito com sucesso', text_color='green')
                sleep(1)
                self.destroy()

                #abre a janela principal
                main_app = Main_app()
                main_app.mainloop()
            else:
                 self.status_label.configure(text='Login Incorreto!', text_color='red')
            

class Main_app(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Tarefas")
        self.geometry("600x500")

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

         # Frame para adicionar nova tarefa
        self.add_task_frame = ctk.CTkFrame(self)
        self.add_task_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.task_entry = ctk.CTkEntry(self.add_task_frame, placeholder_text="Digite uma nova tarefa...")
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.add_button = ctk.CTkButton(self.add_task_frame, text="Adicionar", command=self.add_task)
        self.add_button.pack(side="right")

        # Frame para conter a lista de tarefas
        self.tasks_container_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.tasks_container_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.task_widgets = []
        self.add_task_widget("Comprar pão", False)
        self.add_task_widget("Fazer exercício", True)
        self.add_task_widget("Reunião às 10h", False)

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            self.add_task_widget(task_text, False)
            self.task_entry.delete(0, ctk.END)

    def add_task_widget(self, task_text, completed):
        task_frame = ctk.CTkFrame(self.tasks_container_frame, fg_color="transparent")
        task_frame.pack(fill="x", pady=2)

        checkbox = ctk.CTkCheckBox(task_frame, text=task_text)
        checkbox.pack(side="left", padx=5)
        if completed:
            checkbox.select()
        else:
            checkbox.deselect()

        remove_button = ctk.CTkButton(task_frame, text="X", width=30, command=lambda: self.remove_task_widget(task_frame))
        remove_button.pack(side="right", padx=5)
        self.task_widgets.append(task_frame)

    def remove_task_widget(self, task_frame_to_remove):
        task_frame_to_remove.destroy()
        self.task_widgets.remove(task_frame_to_remove)

# --- Ponto de Entrada da Aplicação ---
if __name__ == "__main__":
    # Inicia a primeira tela (tela de login)
    login_app = Login()
    login_app.mainloop()



"""def validar_login():
    usuario = campo_usuario.get()
    senha = campo_senha.get()

    for _, v in enumerate(pega_dados()):
            if usuario == v[1] and senha == v[2]:
                resultado_login.configure(text='Login feito com sucesso', text_color='green')
                sleep(2)
                ctk.destroy()
                janela_inicial()
            else:
                 resultado_login.configure(text='Login Incorreto!', text_color='red')
            
def janela_inicial():
    '''Janela inicial de tarefas'''

    class App(ctk.CTk):
        def __init__(self):
            super().__init__()

            self.title("Lista de Tarefas")
            self.geometry("500x400") # Define o tamanho inicial da janela

        # Configura o grid para expandir corretamente
            self.grid_rowconfigure(0, weight=0) # Linha para o título/entrada de nova tarefa
            self.grid_rowconfigure(1, weight=1) # Linha para o frame de tarefas (lista)
            self.grid_columnconfigure(0, weight=1)

        # Frame para adicionar nova tarefa
            self.add_task_frame = ctk.CTkFrame(self)
            self.add_task_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

            self.task_entry = ctk.CTkEntry(self.add_task_frame, placeholder_text="Digite uma nova tarefa...")
            self.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 5)) # Expandir o campo de entrada

            self.add_button = ctk.CTkButton(self.add_task_frame, text="Adicionar", command=self.add_task)
            self.add_button.pack(side="right")

        # Frame para conter a lista de tarefas
            self.tasks_container_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
            self.tasks_container_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        # Lista para armazenar as referências aos frames das tarefas (para fácil remoção)
            self.task_widgets = []

        # Exemplo de tarefas iniciais (opcional)
            self.add_task_widget("Comprar leite", False)
            self.add_task_widget("Estudar CustomTkinter", True)
            self.add_task_widget("Pagar contas", False)

    def add_task(self):
        task_text = self.task_entry.get().strip() # Obter texto e remover espaços em branco
        if task_text: # Só adiciona se o texto não estiver vazio
            self.add_task_widget(task_text, False) # Adiciona a nova tarefa
            self.task_entry.delete(0, ctk.END) # Limpa o campo de entrada

    def add_task_widget(self, task_text, completed):
        # Cria um CTkFrame para cada linha de tarefa
        task_frame = ctk.CTkFrame(self.tasks_container_frame, fg_color="transparent")
        task_frame.pack(fill="x", pady=2) # Preenche a largura do container, com um pequeno padding vertical

        # Checkbox
        checkbox = ctk.CTkCheckBox(task_frame, text=task_text)
        checkbox.pack(side="left", padx=5)

        # Definir estado inicial do checkbox
        if completed:
            checkbox.select()
        else:
            checkbox.deselect()

        # Botão para remover a tarefa
        remove_button = ctk.CTkButton(task_frame, text="X", width=30, command=lambda: self.remove_task_widget(task_frame))
        remove_button.pack(side="right", padx=5)

        # Armazena a referência para o frame da tarefa
        self.task_widgets.append(task_frame)

    def remove_task_widget(self, task_frame_to_remove):
        task_frame_to_remove.destroy() # Destrói o frame e todos os seus widgets filhos
        self.task_widgets.remove(task_frame_to_remove) # Remove da nossa lista de referências

    if __name__ == "__main__":
        app = App()
        app.mainloop()


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
app.mainloop()"""