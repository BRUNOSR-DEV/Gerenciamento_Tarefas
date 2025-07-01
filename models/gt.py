import MySQLdb

import sqlite3

def conectar():
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


def pega_dados():
    """
    Função que retorna lista de usuarios e seus dados
    """
    conn= conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuario')
    usuarios = cursor.fetchall()

    if usuarios:
        desconectar(conn)
        return usuarios
    else:
        desconectar(conn)
        return 'Não tem usuários cadastrados'


def pega_id(usuario): 
    '''função que busca id do usuário no bd e retorna a mesma'''  
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(f"SELECT id FROM usuario WHERE nome_usuario = '{usuario}'")
    result = cursor.fetchone()
    desconectar(conn)

    return result
    return result['id'] if result else None



def inserir_usuario(usuario, senha):
    """
    Função para inserir um usuário novo
    """  
    conn = conectar()
    cursor = conn.cursor()


    cursor.execute(f"INSERT INTO usuario (nome_usuario, senha) VALUES ('{usuario}',{senha})")
    conn.commit()
    
    if cursor.rowcount == 1: #retorna o número de linhas afetadas pela última operação executada.
        desconectar(conn)
        return True
    else:
        desconectar(conn)
        return False


def inserir_tarefas(descricao, id_usuario, checkbox):
    """Função que inseri novas tarefas, retornando id da tarefa criada"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO tarefas (descricao, fk_usuario, checkbox) VALUES ('{descricao}', {id_usuario}, {checkbox})")
    conn.commit()

    cursor.execute(f"SELECT id FROM tarefas WHERE descricao='{descricao}' AND fk_usuario= {id_usuario};")
    result = cursor.fetchone()
    
    
    
    if cursor.rowcount == 1: #retorna o número de linhas afetadas pela última operação executada.
        desconectar(conn)
        return result
    else:
        desconectar(conn)
        return 'ID da tarefa não encontrado no BD - (Inserir_tarefas)'
    
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


def listar_tarefas(id_usuario):
    
    conn = conectar()
    cursor = conn.cursor()

    try:
        # CORREÇÃO: Usar placeholder %s e passar id_usuario como tupla
        cursor.execute("SELECT id, descricao, checkbox FROM tarefas WHERE fk_usuario = %s", (id_usuario,))
        tarefas = cursor.fetchall() # Use fetchall() para obter todas as linhas
        return [(t[0], t[1], t[2]) for t in tarefas] # Se o row_factory não estiver definido, acesse por índice
    except Exception as e: # Capture exceções para depuração
        print(f"Erro ao listar tarefas: {e}")
        return [] # Retorne uma lista vazia em caso de erro
    finally:
        desconectar(conn)
        


def deletar_tarefa(tarefa_id):


    conn = conectar()
    cursor = conn.cursor()

    descricao = cursor.execute(f'SELECT descricao FROM tarefas WHERE id={tarefa_id}')
    cursor.execute(f"DELETE FROM tarefas WHERE descricao='{tarefa_id}'")

    if cursor.rowcount == 1: 
        print(f'Produto {descricao} excluído com sucesso.')
    else:
         print(f'Erro ao excluir o produto {descricao}')

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


def atualizar_checkbox(tarefa_id, novo_status):

    conn = conectar()
    cursor = conn.cursor()


    cursor.execute(f"UPDATE tarefas SET checkbox = {novo_status} WHERE id = {tarefa_id} ")
    conn.commit()

    if cursor.rowcount == 1:
        #print(f'O checkbox foi atualizado com sucesso.')
        desconectar(conn)
        return True
    else:
        #print('Não foi possível atualizar!')
        desconectar(conn)
        return False
    
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


def atualizar():
    """
    Função para atualizar um produto
    """
    conn = conectar()
    cursor = conn.cursor()

    listar()

    att = int(input('Informe o id do produto para atualização: '))

    item = int(input('Informe o que vai ser atualizado: \n[1]nome\n[2] preco\n[3]estoque: '))

    if item == 1:
        valor = input('Informe o novo nome: ') 
        cursor.execute(f"UPDATE produtos set nome = '{valor}' WHERE id = {att} ")
        conn.commit()
    elif item == 2:
        valor = float(input('Informe o novo preco: '))
        cursor.execute(f"UPDATE produtos set preco = {valor} WHERE id = {att} ")
        conn.commit()
    elif item == 3:
        valor = int(input('Informe o novo número do estoque: ')) 
        cursor.execute(f"UPDATE produtos set estoque = {valor} WHERE id = {att} ")
        conn.commit()
    else:
        print('Valor incorreto!')
        atualizar()
    
    if cursor.rowcount == 1:
        print(f'O dado {valor} foi inserido com sucesso. att bem sucedido')
    else:
        print('Não foi possível atualizar o valor.')

    desconectar(conn)

    continuar = input('Quer alterar outro valor? [s]sim [n]Menu')
    if continuar == 's' or continuar == 'S':
        atualizar()
    else:
        menu()


def deletar():
    """
    Função para deletar um produto
    """
    conn = conectar()
    cursor = conn.cursor()

    codigo = int(input('Informe o id para deletar o item: '))

    cod_verificado = int(input(f'Deseja realmente apagar o produto {busca_nome(codigo)} \n[1]Sim\n[2]Não :'))

    if cod_verificado == 1:
        cursor.execute(f'DELETE FROM produtos WHERE id={codigo}')
        conn.commit()

        if cursor.rowcount == 1: 
            print('Produto excluído com sucesso.')
        else:
            print(f'Erro ao excluir o produto {busca_nome(codigo)}')
        
            
    elif cod_verificado == 2:
        deletar()
    else:
        print('Valor não correspondente, ou não existe no banco de dados')
        deletar()