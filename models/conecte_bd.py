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
    gerenciar_conn = False

    if conn is None:
        conn= conectar_bd_original()
        gerenciar_conn = True

    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM usuario')
        usuarios = cursor.fetchall()

        if usuarios:
            return usuarios
        else:
            return []
            return 'Não tem usuários cadastrados'
        
    except MySQLdb.Error as e: # Captura erro específico do MySQL
        print(f'Erro no MySQL ao pegar dados: {e}')
        raise # Re-levanta a exceção para que o chamador saiba que algo deu errado

    except Exception as e:
        print(f'Erro inesperado ao pegar dados: {e}')

    finally:
        if gerenciar_conn:
            desconectar(conn)



def pega_id(usuario, conn=None): 
    '''função que busca id do usuário no bd e retorna a mesma''' 

    gerenciar_conn = False

    if conn is None:
        conn = conectar_bd_original()
        gerenciar_conn= True

    cursor = conn.cursor() 

    try:
        sql = "SELECT id FROM usuario WHERE nome_usuario = %s" 
        cursor.execute(sql, (usuario,)) #obs. obrigatório passar uma tupla como parâmetro para cursor
        result = cursor.fetchone()

        if result:
            return result[0]
        
    except MySQLdb.Error as e:
        print(f"Erro MySQL ao pegar ID: {e}")
        return None # Retorna None em caso de erro no DB  
    except Exception as e:
        print(f"Erro inesperado ao pegar ID: {e}")

    finally:
        if gerenciar_conn:
            desconectar(conn)




def inserir_usuario(usuario, senha, conn=None):
    """
    Função para inserir um usuário novo
    """  
    gerenciar_conn = False

    if conn is None:
        conn= conectar_bd_original()
        gerenciar_conn = True

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
        
    except MySQLdb.Error as e:
        print(f'Erro MySQL ao inserir usuário: {e}')
        conn.rollback()
        return False     
    
    except Exception as e:
        print(f'Erro em inserir usuário {e}')
        conn.rollback()
        return False
        
    finally:
        if gerenciar_conn:
            desconectar(conn)
    
    

def inserir_tarefas(descricao, id_usuario, checkbox, conn=None):
    gerenciar_conn = False
    if conn is None:
        conn = conectar_bd_original()
        gerenciar_conn = True

    cursor = conn.cursor()
    try:
        sql = "INSERT INTO tarefas (descricao, fk_usuario, checkbox) VALUES (%s, %s, %s)"
        cursor.execute(sql, (descricao, id_usuario, checkbox))
        conn.commit()
        return cursor.lastrowid # Retorna o ID da tarefa recém-inserida
    
    except MySQLdb.Error as e: # Captura erro específico do MySQL
        print(f"Erro MySQL ao inserir tarefa: {e}")
        conn.rollback()
        return None # Retorna None para indicar falha
    
    except Exception as e:
        print(f"Erro inesperado ao inserir tarefa: {e}")
        conn.rollback()
        return None
        
    finally:
        if gerenciar_conn:
            desconectar(conn)

    
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
    
    gerenciar_conn = False

    if conn is None:
        conn= conectar_bd_original()
        gerenciar_conn= True

    cursor = conn.cursor()

    try:
        # CORREÇÃO: Usar placeholder %s e passar id_usuario como tupla
        cursor.execute("SELECT id, descricao, checkbox FROM tarefas WHERE fk_usuario = %s", (id_usuario,))
        tarefas = cursor.fetchall() # fetchall() para obter todas as linhas, retorna tupla de tuplas 

        return [(t[0], t[1], t[2]) for t in tarefas] # Se o row_factory não estiver definido, acesse por índice
    
    except MySQLdb.Error as e:
        print(f"Erro MySQL ao listar tarefas: {e}")
        return [] # Retorna lista vazia em caso de erro no DB
    except Exception as e: # Capture exceções para depuração
        print(f"Erro ao listar tarefas: {e}")
        return [] # Retorne uma lista vazia em caso de erro geral
    
    finally:
        if gerenciar_conn:
            desconectar(conn)
        


def deletar_tarefa(tarefa_id, conn=None):

    gerenciar_conn = False

    if conn is None:
        conn = conectar_bd_original()
        gerenciar_conn = True

    cursor = conn.cursor()
    try:
        sql = "DELETE FROM tarefas WHERE id = %s"
        cursor.execute(sql, (tarefa_id,))
        conn.commit()
        return cursor.rowcount > 0 # Retorna True se deletou, False caso contrário
    
    except MySQLdb.Error as e:
        print(f"Erro MySQL ao deletar tarefa ID {tarefa_id}: {e}")
        conn.rollback()
        return False
    except Exception as e:
        print(f"Erro inesperado ao tentar deletar tarefa ID {tarefa_id}: {e}")
        conn.rollback()
        return False
    
    finally:
        if gerenciar_conn:
            desconectar(conn)

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
    
    gerenciar_conn = False

    if conn is None:
        conn = conectar_bd_original()
        gerenciar_conn = True

    cursor = conn.cursor()
    try:
        sql = "UPDATE tarefas SET checkbox = %s WHERE id = %s"
        cursor.execute(sql, (novo_status, tarefa_id,))
        conn.commit()
        return cursor.rowcount > 0 # Retorna True se atualizou, False caso contrário
    except MySQLdb.Error as e:
        print(f"Erro MySQL ao atualizar checkbox - ID {tarefa_id}: {e}")
        conn.rollback()
        return False
    except Exception as e:
        print(f"Erro inesperado ao tentar atualizar checkbox - ID {tarefa_id}: {e}")
        conn.rollback()
        return False
    finally:
        if gerenciar_conn:
            desconectar(conn)
    
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


