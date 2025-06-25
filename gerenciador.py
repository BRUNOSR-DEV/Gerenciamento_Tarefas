from models.gt import pega_dados, inserir_usuario

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
        self.geometry('350x400')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=0)

        self.label = ctk.CTkLabel(self, text="Faça seu Login", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, pady=20)

        self.usuario_entry = ctk.CTkEntry(self, placeholder_text="Usuário")
        self.usuario_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.senha_entry = ctk.CTkEntry(self, placeholder_text="Senha", show="*")
        self.senha_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.login = ctk.CTkButton(self, text="Entrar", command=self.validar_login)
        self.login.grid(row=3, column=0, padx=20, pady=10)

        self.registrar = ctk.CTkButton(self, text="Registar", command=self.abrir_tela_registro)
        self.registrar.grid(row=4, column=0, padx=20, pady=10)

        self.status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.status_label.grid(row=5, column=0, pady=5)

    def validar_login(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()
        login_sucesso = False

        for _, v in enumerate(pega_dados()):
            if usuario == v[1] and senha == v[2]:
                login_sucesso = True
                break
         
        if login_sucesso:
            self.status_label.configure(text='Login feito com sucesso', text_color='green')
            self.update_idletasks() # Atualiza a UI para mostrar a mensagem
            sleep(2)
            self.destroy()

            # Abre a janela principal (Gerenciador de Tarefas)
            main_app = Main_app()
            main_app.mainloop()
        else:
            self.status_label.configure(text='Login Incorreto!', text_color='red')

    def abrir_tela_registro(self):
        # Passa a própria instância da tela de login para a tela de registro
        register_window = Registro_usuario(self, login_instance=self)
        #self.status_label.configure(text='Abrindo tela de registro...', text_color='blue')
        
        # A mainloop() não é chamada para toplevels, elas são gerenciadas pelo master.
        self.wait_window(register_window) # Opcional: Pausa a janela de login até a popup fechar



class Registro_usuario(ctk.CTkToplevel):

    def __init__(self,  master=None, login_instance=None):
        super().__init__(master)

        self.master = master # A referência à janela pai (opcional, mas útil)
        self.login_instance = login_instance


        self.title("Registrar Novo Usuário")
        self.geometry("350x400")
        self.transient(master) # Faz a popup aparecer sobre a janela principal e fechar com ela
        self.grab_set() # Bloqueia interações com a janela principal enquanto a popup está aberta
        self.focus_set() # Define o foco para esta janela

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=0)

        ctk.CTkLabel(self, text="Crie sua nova conta", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, pady=15)

        self.novo_usuario = ctk.CTkEntry(self, placeholder_text="Novo Usuário")
        self.novo_usuario.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.nova_senha = ctk.CTkEntry(self, placeholder_text="Nova Senha", show="*")
        self.nova_senha.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.rep_nova_senha = ctk.CTkEntry(self, placeholder_text="Repita a senha", show="*")
        self.rep_nova_senha.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.botao_registrar = ctk.CTkButton(self, text="Confirmar Registro", command=self.processar_registro)
        self.botao_registrar.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.status_label.grid(row=5, column=0, pady=5)

    def processar_registro(self):
        
        usuario = self.novo_usuario.get().strip()
        senha1 = self.nova_senha.get().strip()
        senha2 = self.rep_nova_senha.get().strip()

        if not usuario or not senha1 or not senha2:
            self.status_label.configure(text='Por favor, preencha todos os campos!', text_color='red')
            self.update_idletasks()
            return

        if senha1 == senha2:
            retorno = inserir_usuario(usuario, senha1)

            if retorno:
                self.status_label.configure(text='Os dados foram inseridos com sucesso!', text_color='green')
                self.update_idletasks()
                sleep(4)
                self.destroy()
            else:
                self.status_label.configure(text='Não foi possível registrar, contate o adm do sistema...', text_color='red')
                self.update_idletasks()
        else:
            self.status_label.configure(text='As senhas não correspondem!', text_color='red')
            self.update_idletasks()




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

        self.tarefa_entry = ctk.CTkEntry(self.add_task_frame, placeholder_text="Digite uma nova tarefa...")
        self.tarefa_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.add_botao = ctk.CTkButton(self.add_task_frame, text="Adicionar", command=self.add_tarefa)
        self.add_botao.pack(side="right")

        # Frame para conter a lista de tarefas
        self.tasks_container_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.tasks_container_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.task_widgets = []
        self.add_task_widget("Comprar pão", False)
        self.add_task_widget("Fazer exercício", True)
        self.add_task_widget("Reunião às 10h", False)

    def add_tarefa(self):
        tarefa_text = self.tarefa_entry.get().strip()
        if tarefa_text:
            self.add_task_widget(tarefa_text, False)
            self.tarefa_entry.delete(0, ctk.END)

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