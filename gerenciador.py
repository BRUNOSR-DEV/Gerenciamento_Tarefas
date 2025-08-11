"""
 ------------------ Introdução do projeto ------------------------

 - A app utiliza a biblioteca CustomTkinter como interface gráfica. 
 - Utiliza também MySQL como banco de dados.
 - Todos recursos/bibliotecas foram instalados no ambiente virtual (vir_gt).
 - A pasta "models.py" contem o arquivo "conecte_bd" que faz a conexão com banco de dados, realizando as operações necessárias.
 - O "gerenciador.py" é o arquivo de main de execução do programa, com todas as classes e métodos necessários para execução do programa...
----------------------------------------------------------------------

"""

#import dos métodos para conexão 
from models.conecte_bd import (
    pega_dados, inserir_usuario, pega_id, inserir_tarefas, deletar_tarefa, atualizar_checkbox, listar_tarefas
    )
from time import sleep
import customtkinter as ctk


#configura a aparência
ctk.set_appearance_mode('dark')


#Criação das funções de funcionalidades
class Login(ctk.CTk):
    """Classe Login herda de ctk.CTK - configura a interface para receber os dados do usuário e faz a verificação no BD."""

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
        """ Valida o login que o usuário inseriu na entry"""
        
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
        """ Direciona o usuário para fazer cadastro chamando a classe Registro_usuario"""
        
        # Passa a própria instância da tela de login para a tela de registro
        register_window = Registro_usuario(self, login_instance=self)
        #self.status_label.configure(text='Abrindo tela de registro...', text_color='blue')
        
        # A mainloop() não é chamada para toplevels, elas são gerenciadas pelo master.
        self.wait_window(register_window) #Pausa a janela de login até a popup fechar



class Registro_usuario(ctk.CTkToplevel):
    """Classe para registro: configuração da interface para receber dados e a inserção dos dados no BD. (inserir_usuario)"""

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
        """Processa o registro - pega os dados inseridos, verifica e guarda no BD"""
        
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
    """ Classe Main - app principal, configuração de interface, listamento de tarefas do BD. Intereção com app, atualição, delete, inserção... (CRUD)"""

    def __init__(self, logged_in_username=None):
        super().__init__()
        self.title("Gerenciador de Tarefas")
        self.geometry("600x500")

        self.__dict__['usuario_logado'] = logged_in_username
        
        self.user_id = pega_id(self.usuario_logado)

        self.grid_rowconfigure(0, weight=0) # Linha para o frame superior (usuário e add tarefa)
        self.grid_rowconfigure(1, weight=1) # Linha para o frame de tarefas rolavel
        self.grid_columnconfigure(0, weight=1)

        # Frame superior para o nome do usuário e a área de adicionar tarefa
        self.top_section_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_section_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.top_section_frame.grid_columnconfigure(0, weight=0) # primeira coluna para label usuário
        self.top_section_frame.grid_columnconfigure(0, weight=1) # segunda coluna para botão sair

        # Label para exibir o nome do usuário
        if self.usuario_logado: 
            self.username_label = ctk.CTkLabel(self.top_section_frame,
                                               text=f"Bem-vindo, {self.usuario_logado}!",
                                               font=ctk.CTkFont(size=16, weight="bold"))
            
        else:
            self.username_label = ctk.CTkLabel(self.top_section_frame,
                                               text="Bem-vindo!",
                                               font=ctk.CTkFont(size=16, weight="bold"))
            
        self.botao_sair = ctk.CTkButton(self.top_section_frame, text="Sair", command=self.voltar_Plogin, width=80,
                                        fg_color="#FF0000", hover_color="#810000")
        
        self.botao_sair.grid(row=0, column=1,sticky="e") #coluna 1 alinhado a direita

        #Primeira Label da janela de tarefas    
        self.username_label.grid(row=0, column=0, pady=(0, 10), sticky="w")
        

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
        self.tasks_container_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.task_widgets_data = []

        self.carregar_bd()


    
    def carregar_bd(self):
        """ Busca as tarefas do usuário que fez o login, passando o id do mesmo"""

        """ código para quando o método carregar_bd for chamado em outra 'situação'"
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

            nova_tarefa_id = inserir_tarefas(tarefa_text, self.user_id, 0)

            if nova_tarefa_id:
                self._cria_add_tarefa(nova_tarefa_id, tarefa_text, 0)# só aparece a tarefa na interface se salvou no BD
                self.tarefa_entry.delete(0, ctk.END) # Limpa o campo entry apenas se salvou no BD
            else:
                print('Erro: Não foi possível salvar a tarefa no banco de dados.')

            
    def _cria_add_tarefa(self, tarefa_id, tarefa_text, concluida_status):
        """
        Cria e adiciona um widget de tarefa à UI.
        Este método é interno e chamado por add_task e load_tasks_from_db.
        """

        task_frame = ctk.CTkFrame(self.tasks_container_frame, fg_color="transparent")
        task_frame.pack(fill="x", pady=2)

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


    def voltar_Plogin(self):

        self.username_label.configure(text=f'Até a próxima {self.usuario_logado} !', text_color='red')
        self.update_idletasks()

        sleep(3)

        self.destroy()
        from gerenciador import Login

        login_app = Login()
        login_app.mainloop()



# --- Ponto de Entrada da Aplicação ---
if __name__ == "__main__":
    # Inicia a primeira tela (tela de login)
    login_app = Login()
    login_app.mainloop()

