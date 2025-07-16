import MySQLdb


def conectar_bd_original():
    """
    Função para conectar ao servidor
    """
    try:
        conn = MySQLdb.connect(
            db= 'gerenciador_tarefas',
            host= 'localhost',
            user= 'hey',
            passwd= 'boney',
        )
        return conn

    except MySQLdb.Error as e:
        print(f'Erro na conexão ao MySql Server: {e}')



def desconectar(conn):
    """ 
    Função para desconectar do servidor.
    """
    if conn:
        conn.close()



def pega_dados(conn=None):
    """
    Função que retorna lista de usuarios e seus dados
    """
    if conn is None:
        conn= conectar_bd_original()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM usuario')
        usuarios = cursor.fetchall()

        if usuarios:
            desconectar(conn)
            return usuarios
        else:
            desconectar(conn)
            return 'Não tem usuários cadastrados'



def pega_id(usuario, conn=None): 
    '''função que busca id do usuário no bd e retorna a mesma''' 

    if conn is None:
        conn = conectar_bd_original()
        cursor = conn.cursor() 


        sql = "SELECT id FROM usuario WHERE nome_usuario = %s" 
        cursor.execute(sql, (usuario,)) #obs. obrigatório passar uma tupla como parâmetro para cursor
        result = cursor.fetchone()
        desconectar(conn)

        return result
        return result['id'] if result else None



def inserir_usuario(usuario, senha, conn=None):
    """
    Função para inserir um usuário novo
    """  
    if conn is None:
        conn= conectar_bd_original()
        cursor = conn.cursor()
        sucesso = False

        try:

            cursor.execute("INSERT INTO usuario (nome_usuario, senha) VALUES (%s, %s)",(usuario, senha))
            conn.commit()

            if cursor.rowcount == 1: #retorna o número de linhas afetadas pela última operação executada.
                print(f'Usuário inserido com sucesso! {usuario}')
                sucesso = True
                return sucesso 
            else:
                print('Não foi possível inserir usuário no banco de dados! ')
                sucesso = False
                return sucesso
            
        except Exception as e:
            print('Erro em inserir usuário {e}')
            conn.rollback()
            return None
        
        finally:
            desconectar(conn)
    
    

def inserir_tarefas(descricao, id_usuario, checkbox, conn=None):
    
    if conn is None:
        conn= conectar_bd_original()
        cursor = conn.cursor()

        try:
            # 1. Usar placeholder %s para todos os valores
            # 2. Passar os valores como uma tupla no segundo argumento de execute()
            sql = "INSERT INTO tarefas (descricao, fk_usuario, checkbox) VALUES (%s, %s, %s)"
            cursor.execute(sql, (descricao, id_usuario, checkbox))
            conn.commit()
            # Assumindo que você quer o ID da tarefa recém-inserida
            return cursor.lastrowid # Retorna o ID da última linha inserida
        
        except Exception as e: # Captura exceções para depuração

            print(f"Erro ao inserir tarefa: {e}")
            conn.rollback() # Reverte a transação em caso de erro
            return None # Retorna None para indicar falha
        finally:

            if cursor.rowcount == 1: #retorna o número de linhas afetadas pela última operação executada.
                desconectar(conn)
                print('Tarefa inserida com sucesso!') 
            else:
                desconectar(conn)
                print('ID da tarefa não encontrado no BD - (Inserir_tarefas)')

    
    ''' ------outra forma de se fazer---------
    
    def inserir_tarefas(descricao_tarefa, id_usuario, status_concluida):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO tarefas (descricao, id_usuario, concluida) VALUES (?, ?, ?)",
                       (descricao_tarefa, id_usuario, status_concluida))
        conn.commit()
        return cursor.lastrowid # Retorna o ID da última linha inserida
    except sqlite3.Error as e:
        print(f"Erro ao inserir tarefa: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()'''



def listar_tarefas(id_usuario, conn=None):
    
    if conn is None:
        conn= conectar_bd_original()
        cursor = conn.cursor()

        try:
            # CORREÇÃO: Usar placeholder %s e passar id_usuario como tupla
            cursor.execute("SELECT id, descricao, checkbox FROM tarefas WHERE fk_usuario = %s", (id_usuario,))
            tarefas = cursor.fetchall() # fetchall() para obter todas as linhas, retorna tupla de tuplas 

            return [(t[0], t[1], t[2]) for t in tarefas] # Se o row_factory não estiver definido, acesse por índice
        except Exception as e: # Capture exceções para depuração
            print(f"Erro ao listar tarefas: {e}")
            return [] # Retorne uma lista vazia em caso de erro
        finally:
            desconectar(conn)
        


def deletar_tarefa(tarefa_id, conn=None):
    
    if conn is None:
        conn= conectar_bd_original()
        cursor = conn.cursor()
        sucesso = False 

        try:
            print(f"DEBUG: Tentando deletar tarefa com ID: {tarefa_id}") # Para depuração
            sql = "DELETE FROM tarefas WHERE id = %s" # Espaço após '=' é boa prática, mas não obrigatório
            cursor.execute(sql, (tarefa_id,))

            conn.commit() 

            if cursor.rowcount == 1:
                print(f'Tarefa com ID {tarefa_id} excluída com sucesso do banco de dados.')
                sucesso = True
            else:
                # Isso pode acontecer se o ID não existir no banco de dados
                print(f'Erro ao excluir tarefa com ID {tarefa_id}. Nenhuma linha afetada ou ID não encontrado.')
                sucesso = False

        except Exception as e:
            print(f"DEBUG: Erro inesperado ao tentar deletar tarefa ID {tarefa_id}: {e}")
            conn.rollback() # Desfaz as alterações em caso de erro
            sucesso = False
        finally:
            desconectar(conn)
        return sucesso

    """ ----------- forma mais correta ------------

    def deletar_tarefa(id_tarefa):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao deletar tarefa: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()"""



def atualizar_checkbox(tarefa_id, novo_status, conn=None):

    if conn is None:
        conn= conectar_bd_original()
        cursor = conn.cursor()
        sucesso = False

        try:
            cursor.execute("UPDATE tarefas SET checkbox = %s WHERE id = %s", (novo_status, tarefa_id,))
            conn.commit()

            if cursor.rowcount == 1:
                #print(f'O checkbox foi atualizado com sucesso.')
                sucesso = True
                return sucesso
            else:
                #print('Não foi possível atualizar!')
                sucesso = False
                return sucesso
            
        except Exception as e:

            print(f"DEBUG: Erro inesperado ao tentar atualizar checkbox - ID {tarefa_id}: {e}")
            conn.rollback()

        finally:
            desconectar(conn)

        return sucesso
    
    """------ forma mais correta --------------

    def atualizar_status_tarefa(id_tarefa, status_concluida):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE tarefas SET concluida = ? WHERE id = ?",
                       (status_concluida, id_tarefa))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao atualizar status: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()"""


