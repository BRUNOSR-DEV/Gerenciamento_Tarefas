"""
Módulo de Testes Unitários - Gerenciador de Tarefas.

Este script utiliza o framework 'unittest' para validar as operações de CRUD
(Create, Read, Update, Delete) no banco de dados MySQL.

ATENÇÃO: Este script realiza operações destrutivas (DELETE). 
Certifique-se de que o 'teste_config.ini' aponta para um banco de dados de TESTE, 
e não para o banco de dados principal da aplicação 'config.ini'.
"""

import unittest
import MySQLdb

import configparser 


from models.conecte_bd import (
    desconectar, inserir_usuario,
    inserir_tarefas, pega_id, listar_tarefas, deletar_tarefa,
    atualizar_checkbox, verifica_login, 
)



def conectar_teste():
    """
    Estabelece conexão exclusiva para o ambiente de testes lendo o teste_config.ini
    """
    config = configparser.ConfigParser()
    config.read('teste_config.ini')
    
    if 'mysql' not in config:
        print("Erro: Arquivo config_teste.ini ou seção [mysql] não encontrada.")
        return None

    bd_config = config['mysql']

    try:
        conn = MySQLdb.connect(
            db=bd_config.get('db'),
            host=bd_config.get('host', 'localhost'),
            user=bd_config.get('user'),
            passwd=bd_config.get('passwd')
        )
        return conn

    except MySQLdb.Error as e:
        print(f'Erro na conexão ao MySQL Server de TESTE: {e}')
        raise


def limpar_tabelas(conn):
    """
    Limpa os dados das tabelas para garantir um ambiente isolado em cada teste.
    
    Trava de Segurança: Só executa o DELETE se o nome do banco de dados
    terminar com '_teste' ou '_test', evitando apagar dados reais acidentalmente.
    """
    cursor = conn.cursor()
    
    # Busca o nome do banco de dados atual para a trava de segurança
    cursor.execute("SELECT DATABASE()")
    db_name = cursor.fetchone()[0]

    if "teste" not in db_name.lower():
        raise Exception(
            f"TRAVA DE SEGURANÇA: O banco conectado '{db_name}' não parece ser um banco de testes. "
            "Operação de limpeza abortada para evitar perda de dados reais."
        )

    try:
        # Desativa temporariamente a checagem de chave estrangeira para limpar sem erros
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("DELETE FROM tarefas")
        cursor.execute("DELETE FROM usuario")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit() 
    except MySQLdb.Error as e:
        print(f"Erro ao limpar tabelas de teste: {e}")
        conn.rollback()
        raise


class TestGerenciadorTarefas(unittest.TestCase):
    """
    Suite de testes para validar a integridade da camada de persistência.
    """

    # Este método é executado ANTES de CADA teste
    def setUp(self):
        """Método executado ANTES de cada teste para preparar o ambiente."""
        self.conn = conectar_teste()
        # Limpa as tabelas antes de cada teste para garantir um estado limpo
        limpar_tabelas(self.conn) 
        print(f"\n--- Configurando teste: {self._testMethodName} ---")


    def tearDown(self):
        """Método executado DEPOIS de cada teste para liberar recursos."""
        if self.conn:
            self.conn.close()
        print(f"--- Limpando após teste: {self._testMethodName} ---")


    def test_inserir_usuario_e_pegar_id(self):
        """Verifica se um usuário é inserido corretamente e retorna um ID válido."""

        self.assertTrue(inserir_usuario("testuser_unit", "senha123", self.conn))
        user_id = pega_id("testuser_unit", self.conn)
        self.assertIsNotNone(user_id)
        self.assertGreater(user_id, 0) # ID deve ser maior que 0

    def test_verifica_login(self):
        """ Verifica se usuário e senha insereido esta no banco de dados e retorna True"""

        #inserindo usuario no bd de teste
        inserir_usuario("testuser", "senha123", self.conn)

        self.assertTrue(verifica_login("testuser", "senha123" , self.conn ))
        
        self.assertFalse(verifica_login("testuser", "senha_errada", self.conn))
        self.assertFalse(verifica_login("test_errado", "senha123", self.conn))

    def test_inserir_tarefas(self):
        """Valida a inserção de uma nova tarefa vinculada a um usuário."""

        inserir_usuario("testuser2", "senha456", self.conn)
        user_id = pega_id("testuser2", self.conn)
        self.assertIsNotNone(user_id)

        tarefa_id = inserir_tarefas("Comprar leite", user_id, 0, self.conn)
        self.assertIsNotNone(tarefa_id)
        self.assertGreater(tarefa_id, 0)

    def test_listar_tarefas(self):
        """Garante que a listagem retorna a quantidade e os dados exatos inseridos."""

        inserir_usuario("testuser3", "senha789", self.conn)
        user_id = pega_id("testuser3", self.conn)

        inserir_tarefas("Tarefa A", user_id, 0, self.conn)
        inserir_tarefas("Tarefa B", user_id, 1, self.conn)

        tarefas = listar_tarefas(user_id, self.conn)
        self.assertEqual(len(tarefas), 2)
        self.assertEqual(tarefas[0][1], "Tarefa A") # Descrição
        self.assertEqual(tarefas[0][2], 0)         # Status
        self.assertEqual(tarefas[1][1], "Tarefa B")
        self.assertEqual(tarefas[1][2], 1)

    def test_deletar_tarefa(self):
        """Confirma se uma tarefa é removida fisicamente do banco de dados."""

        inserir_usuario("testuser4", "senha101", self.conn)
        user_id = pega_id("testuser4", self.conn)
        tarefa_id = inserir_tarefas("Tarefa para deletar", user_id, 0, self.conn)

        self.assertTrue(deletar_tarefa(tarefa_id, self.conn)) # Deve retornar True se sucesso

        tarefas_restantes = listar_tarefas(user_id, self.conn)
        self.assertEqual(len(tarefas_restantes), 0)

    def test_atualizar_status_tarefa(self):
        """Verifica a mudança de estado (checkbox) de uma tarefa."""

        inserir_usuario("testuser5", "senha202", self.conn)
        user_id = pega_id("testuser5", self.conn)
        tarefa_id = inserir_tarefas("Tarefa para atualizar", user_id, 0, self.conn)

        self.assertTrue(atualizar_checkbox(tarefa_id, 1, self.conn)) # Atualiza para concluída

        tarefas = listar_tarefas(user_id, self.conn)
        self.assertEqual(tarefas[0][2], 1) # Verifica se o status foi atualizado

if __name__ == '__main__':
    unittest.main()