from models.gt import pega_dados, inserir_usuario, pega_id, inserir_tarefas, deletar_tarefa, atualizar_checkbox, listar_tarefas

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

        self.botao_enter = ctk.CTkButton(self, text="Entrar", command=self.validar_login, 
                                         fg_color="#000200", hover_color="#FC0404")
        self.botao_enter.grid(row=3, column=0, padx=20, pady=10)
        self.bind("<Return>", lambda event: self.botao_enter.invoke())

        self.registrar = ctk.CTkButton(self, text="Registar", command=self.abrir_tela_registro,
                                       fg_color="#000200", hover_color="#FC0404")
        self.registrar.grid(row=4, column=0, padx=20, pady=10)

        self.status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.status_label.grid(row=5, column=0, pady=5)

    def validar_login(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()
        login_sucesso = False
        usuario_logado = usuario

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
            main_app = Main_app(logged_in_username=usuario_logado)
            main_app.mainloop()
        else:
            self.status_label.configure(text='Login Incorreto!', text_color='red')

    def nome_usuario(self):
        return self.usuario
    

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
            sleep(1)
            return

        if senha1 == senha2:
            retorno = inserir_usuario(usuario, senha1)

            if retorno:
                self.status_label.configure(text='Os dados foram inseridos com sucesso!', text_color='green')
                self.update_idletasks()
                sleep(2)

                self.status_label.configure(text=f'usuário: {usuario} Já pode fazer login no sistema! ', text_color='blue')
                self.update_idletasks()
                sleep(6)

                self.destroy()
            else:
                self.status_label.configure(text='Não foi possível registrar, contate o adm do sistema...', text_color='red')
                self.update_idletasks()
        else:
            self.status_label.configure(text='As senhas não correspondem!', text_color='red')
            self.update_idletasks()



class Main_app(ctk.CTk):
    def __init__(self, logged_in_username=None):
        super().__init__()
        self.title("Gerenciador de Tarefas")
        self.geometry("600x500")

        # Solução para o AttributeError: use __dict__ para definir o atributo
        # E/ou use um nome ligeiramente diferente para evitar conflitos indiretos
        self.__dict__['_app_logged_in_username'] = logged_in_username
        self.user_id = pega_id(self._app_logged_in_username)

        self.grid_rowconfigure(0, weight=0) # Linha para o frame superior (usuário e add tarefa)
        self.grid_rowconfigure(1, weight=1) # Linha para o frame de tarefas rolavel
        self.grid_columnconfigure(0, weight=1)

        # Frame superior para o nome do usuário e a área de adicionar tarefa
        self.top_section_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_section_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.top_section_frame.grid_columnconfigure(0, weight=1) # Para o label se expandir

        # Label para exibir o nome do usuário
        if self._app_logged_in_username: 
            self.username_label = ctk.CTkLabel(self.top_section_frame,
                                               text=f"Bem-vindo, {self._app_logged_in_username}!", # <--- E AQUI!
                                               font=ctk.CTkFont(size=16, weight="bold"))
        else:
            self.username_label = ctk.CTkLabel(self.top_section_frame,
                                               text="Bem-vindo!",
                                               font=ctk.CTkFont(size=16, weight="bold"))
        self.username_label.grid(row=0, column=0, pady=(0, 10), sticky="w") # Posicione o label dentro do top_section_frame

        # Frame para adicionar nova tarefa (dentro do top_section_frame)
        self.add_task_frame = ctk.CTkFrame(self.top_section_frame, fg_color="transparent") # <--- Filho do top_section_frame
        self.add_task_frame.grid(row=1, column=0, padx=0, pady=0, sticky="ew") # <--- Agora na linha 1 dentro de top_section_frame


        self.tarefa_entry = ctk.CTkEntry(self.add_task_frame, placeholder_text="Digite uma nova tarefa...")
        self.tarefa_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.add_button = ctk.CTkButton(self.add_task_frame, text="Adicionar", command=self.add_tarefa,
                                        fg_color="#006400", hover_color="#008000")
        self.add_button.pack(side="right")

        self.bind("<Return>", lambda event: self.add_button.invoke()) # Bind do Enter aqui

        
        # Frame para conter a lista de tarefas (filho da Main_app, na próxima linha)
        self.tasks_container_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.tasks_container_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew") # <--- Agora na linha 1 (da Main_app), pois o top_section_frame está na linha 0. A Main_app tem 2 rows principais.

        self.task_widgets_data = []

        self.carregar_bd()


        """ --- forma antiga -----
        id_usuario = pega_id(self._app_logged_in_username)
        tamanho = len(listar_tarefas(id_usuario))

        for i,v in enumerate(listar_tarefas(id_usuario)):
            self.add_task_widget(v[1], v[0])
            if i+1 == tamanho:
                break
                
            self.add_task_widget("Comprar pão", False)
            self.add_task_widget("Fazer exercício", True)
            self.add_task_widget("Reunião às 10h", False)"""
    
    def carregar_bd(self):

        
        """ código para quando o método carregar_bd for chamado em outra "situação""
        for widget_data in self.task_widgets_data:
            widget_data['frame'].destroy()
        self.task_widgets_data.clear() # Limpa a lista interna também"""

        tarefas = listar_tarefas(self.user_id)
        print(self.user_id)
        print(tarefas)

        if tarefas:
            for tarefa_id, descricao, status in tarefas: # Assumindo (id, descricao, status)
                self._cria_add_tarefa(tarefa_id, descricao, status)




    def add_tarefa(self): 
        '''Pega tarefa inserida no entry e manda para função ...widget, salva tarefa no banco de dados'''

        tarefa_text = self.tarefa_entry.get().strip()

        if tarefa_text:
            # 1. Inserir a nova tarefa no banco de dados
            # Assumindo que inserir_tarefas retorna o ID da tarefa recém-criada
            # e que o status inicial é 0 (não concluída)

            nova_tarefa_id = inserir_tarefas(tarefa_text, self.user_id, 0)

            if nova_tarefa_id:
                # 2. Se a inserção no banco foi bem-sucedida, adicione o widget
                self._cria_add_tarefa(nova_tarefa_id, tarefa_text, 0)
                self.tarefa_entry.delete(0, ctk.END) # Limpa o campo apenas se salvou no DB
            else:
                # Você pode adicionar uma mensagem de erro na UI aqui
                print('Erro: Não foi possível salvar a tarefa no banco de dados.')

            

    def _cria_add_tarefa(self, tarefa_id, tarefa_text, concluida_status):
        """
        Cria e adiciona um widget de tarefa à UI.
        Este método é interno e chamado por add_task e load_tasks_from_db.
        """

        task_frame = ctk.CTkFrame(self.tasks_container_frame, fg_color="transparent")
        task_frame.pack(fill="x", pady=2)

        # Usar IntVar para o checkbox permite rastrear seu estado facilmente
        # e ligar a uma função de comando
        var_checkbox = ctk.IntVar(value=concluida_status)
        checkbox = ctk.CTkCheckBox(task_frame, text=tarefa_text, variable=var_checkbox,
                                   command=lambda tid=tarefa_id, cb_var=var_checkbox: self.status_tarefa(tid, cb_var))
        checkbox.pack(side="left", padx=5)

        # Definir o estado inicial do checkbox
        if concluida_status == 1:
            checkbox.select()
        else:
            checkbox.deselect()

        remove_button = ctk.CTkButton(task_frame, text="X", width=30,
                                       command=lambda tid=tarefa_id, tf=task_frame: self.remove_tarefa(tid, tf))
        remove_button.pack(side="right", padx=5)

        # Armazenar informações sobre a tarefa, incluindo o ID do banco de dados e o frame
        self.task_widgets_data.append({
            'id': tarefa_id,
            'description': tarefa_text,
            'status_var': var_checkbox, # Armazena a variável do checkbox
            'checkbox_widget': checkbox,
            'frame': task_frame
        })


    def status_tarefa(self, tarefa_id, checkbox):

        novo_status = checkbox.get() # 1 se marcado, 0 se desmarcado
        print(f"Tarefa ID: {tarefa_id}, Novo Status: {novo_status}")

        if atualizar_checkbox(tarefa_id, novo_status):
            print(f"Status da tarefa {tarefa_id} atualizado no DB para {novo_status}")
        else:
            print(f"Erro ao atualizar status da tarefa {tarefa_id} no DB.")
            if novo_status == 1:
                checkbox.set(0)
            else:
                checkbox.set(1)


    def remove_tarefa(self, tarefa_id_remove, tarefa_frame_remove):
        
        if deletar_tarefa(tarefa_id_remove):
            tarefa_frame_remove.destroy()
            self.task_widgets_data = [item for item in self.task_widgets_data if item['id'] != tarefa_id_remove]
            print(f"Tarefa ID: {tarefa_id_remove} removida do DB e da UI.")
        else:
            print(f"Erro ao remover tarefa ID: {tarefa_id_remove} do banco de dados.")

            '''deletar_tarefa(task_frame_to_remove)
            self.task_widgets.remove(task_frame_to_remove)'''

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