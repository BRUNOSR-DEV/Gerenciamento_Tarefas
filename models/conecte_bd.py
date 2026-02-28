import MySQLdb

import configparser # Modulo nativo do Py. Ele cria, lê,atualiza e gerencia arq/ de conf/


def ler_configuracao_bd():
    """
    Lê as credenciais do banco de dados do arquivo 'config.ini'.
    
    Busca pela seção [mysql] para garantir que as credenciais 
    não fiquem expostas no código-fonte (Pratica de de segurança).
    
    Returns:
        dict: Dicionário contendo host, user, passwd e db se sucesso.
        None: Caso o arquivo não exista ou a seção esteja ausente.
    """

    config = configparser.ConfigParser() # Instanciando o objeto config
    
    # Tenta ler o arquivo de configuração
    try:
        config.read('config.ini')
        if 'mysql' not in config:
            raise ValueError("Seção [mysql] não encontrada em config.ini")
            
        bd_config = config['mysql']
        return {
            'host': bd_config.get('host', 'localhost'), # se não for "host" define como "localhost"
            'user': bd_config.get('user'),
            'passwd': bd_config.get('passwd'),
            'db': bd_config.get('db')
        }
    except FileNotFoundError:
        print("Erro: Arquivo 'config.ini' não encontrado.")
        return None
    except ValueError as e:
        print(f"Erro de configuração: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado ao ler o arquivo de configuração: {e}")
        return None



def conectar_bd_original():
    """
    Estabelece a conexão com o servidor MySQL utilizando as credenciais.
    
    Returns:
        MySQLdb.connections.Connection: Objeto de conexão se bem-sucedido.
        None: Em caso de falha de leitura de configuração ou recusa do servidor.
    """

    bd_config = ler_configuracao_bd()
    if not bd_config:
        # Se as credenciais não puderam ser lidas, não tente conectar
        print("Não foi possível conectar ao banco de dados devido a um erro de configuração.")
        return None
    
    try:
        conn = MySQLdb.connect(
            db=bd_config['db'],
            host=bd_config['host'],
            user=bd_config['user'],
            passwd=bd_config['passwd']
        )
        return conn

    except MySQLdb.Error as e:
        print(f'Erro na conexão ao MySql Server: {e}')



def desconectar(conn):
    """ 
    Encerra a conexão com o banco de dados de forma segura.
    
    Args:
        conn (MySQLdb.connections.Connection): A conexão ativa atual.
    """
    if conn:
        conn.close()



def pega_dados(conn=None):
    """
    Busca todos os usuários cadastrados no banco de dados.
    
    Args:
        conn (MySQLdb.connections.Connection, optional): Conexão ativa com o banco. 
            Se não fornecida, a função abre e gerencia sua própria conexão.

    Returns:
        list: Lista de tuplas com os dados dos usuários. Retorna uma lista vazia [] 
              se não houver usuários ou em caso de falha não-crítica.
    """

    gerenciar_conn = False

    if conn is None:
        conn= conectar_bd_original()
        gerenciar_conn = True

    cursor = conn.cursor() # Mensageiro, passa o comando e retorna resltados

    try:
        cursor.execute('SELECT * FROM usuario')
        usuarios = cursor.fetchall()

        if usuarios:
            return usuarios
        else:
            return []
        
    except MySQLdb.Error as e: # Captura erro específico do MySQL
        print(f'Erro no MySQL ao pegar dados: {e}')
        raise # Re-levanta a exceção para que o chamador saiba que algo deu errado

    except Exception as e:
        print(f'Erro inesperado ao pegar dados: {e}')

    finally:
        if gerenciar_conn:
            desconectar(conn)



def pega_id(usuario, conn=None): 
    """
    Busca o ID (Chave Primária) de um usuário específico pelo nome.
    
    Args:
        usuario (str): Nome do usuário a ser pesquisado.
        conn (MySQLdb.connections.Connection, optional): Conexão ativa com o banco.

    Returns:
        int: ID do usuário se encontrado.
        None: Caso o usuário não exista ou ocorra um erro na query.
    """

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
        print(f"Erro MySQL ao buscar ID do usuário '{usuario}': {e}")
        return None # Retorna None em caso de erro no DB  
    except Exception as e:
        print(f"Erro inesperado ao pegar ID: {e}")

    finally:
        if gerenciar_conn:
            desconectar(conn)



def inserir_usuario(usuario, senha, conn=None):
    """
    Cadastra um novo usuário no banco de dados.
    
    Args:
        usuario (str): Nome do novo usuário.
        senha (str): Senha do usuário.
        conn (MySQLdb.connections.Connection, optional): Conexão ativa com o banco.

    Returns:
        bool: True se o cadastro foi realizado com sucesso, False caso contrário.
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
    """
    Insere uma nova tarefa no banco de dados vinculada a um usuário.
    
    Args:
        descricao (str): O texto descritivo da tarefa.
        id_usuario (int): O ID do usuário dono da tarefa (Chave Estrangeira).
        checkbox (int/bool): Status inicial da tarefa (ex: 0 para pendente, 1 para concluída).
        conn (MySQLdb.connections.Connection, optional): Conexão ativa com o banco.

    Returns:
        int: O ID da tarefa recém-inserida (útil para a interface gráfica).
        None: Em caso de falha na inserção.
    """
    
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





def listar_tarefas(id_usuario, conn=None):
    """
    Retorna a lista de tarefas associadas a um usuário específico.
    
    Args:
        id_usuario (int): O ID do usuário logado.
        conn (MySQLdb.connections.Connection, optional): Conexão ativa com o banco.

    Returns:
        list: Lista de tuplas contendo (id, descricao, checkbox) de cada tarefa.
              Retorna uma lista vazia [] se não houver tarefas ou se ocorrer erro.
    """
    
    gerenciar_conn = False

    if conn is None:
        conn= conectar_bd_original()
        gerenciar_conn= True

    cursor = conn.cursor()

    try:
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
    """
    Remove uma tarefa do banco de dados utilizando seu ID.

    Args:
        tarefa_id (int): O ID da tarefa a ser deletada.
        conn (MySQLdb.connections.Connection, optional): Conexão ativa com o banco.

    Returns:
        bool: True se a tarefa foi deletada com sucesso, False caso contrário.
    """

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




def atualizar_checkbox(tarefa_id, novo_status, conn=None):
    """
    Atualiza o status de conclusão (checkbox) de uma tarefa.

    Args:
        tarefa_id (int): O ID da tarefa.
        novo_status (int/bool): O novo valor (ex: 1 para checado, 0 para desmarcado).
        conn (MySQLdb.connections.Connection, optional): Conexão ativa com o banco.

    Returns:
        bool: True se a atualização foi bem-sucedida, False caso contrário.
    """
    
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
    


