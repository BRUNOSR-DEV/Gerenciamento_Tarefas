
import unittest
import os
import MySQLdb

from models.conecte_bd import (
    conectar, desconectar, inserir_usuario,
    inserir_tarefas, pega_id, listar_tarefas, deletar_tarefa,
    atualizar_checkbox, pega_dados
)

def conectar():
    """
    Função para conectar ao servidor
    """
    try:
        conn = MySQLdb.connect(
            db= 'teste_bd_gerenciador_tarefas',
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


class TestGerenciadorTarefas(unittest.TestCase):

    def __init__(self):
        super().__init__()
        self.conn= conectar()

    # Este método é executado ANTES de CADA teste
    def setUp(self):
        # Limpa e configura o banco de dados de teste para cada teste
        if os.path.exists(self.conn):
            os.remove(self.conn) # Remove o DB anterior para um estado limpo
        # Sobrescrever conectar para usar o DB de teste
        # Isso pode ser feito passando o nome do DB para conectar ou mockando
        # Para simplicidade, vou chamar as funções de criação diretamente
        self.conn = conectar() # Assumindo que conectar usa TEST_DB_NAME internamente
        #criar_tabela_usuarios()
        #criar_tabela_tarefas()
        desconectar(self.conn)
        print(f"\nConfigurando banco de dados de teste: {self.conn}")

    # Este método é executado DEPOIS de CADA teste
    def tearDown(self):
        # Limpa o banco de dados de teste
        if os.path.exists(self.conn):
            os.remove(self.conn)
        print(f"Limpando banco de dados de teste: {self.conn}")

    def test_inserir_usuario_e_pegar_id(self):
        # Testa se um usuário pode ser inserido e se seu ID pode ser recuperado
        self.assertTrue(inserir_usuario("testuser", "senha123"))
        user_id = pega_id("testuser")
        self.assertIsNotNone(user_id)
        self.assertGreater(user_id, 0) # ID deve ser maior que 0

    def test_inserir_tarefas(self):
        inserir_usuario("testuser2", "senha456")
        user_id = pega_id("testuser2")
        self.assertIsNotNone(user_id)

        tarefa_id = inserir_tarefas("Comprar leite", user_id, 0)
        self.assertIsNotNone(tarefa_id)
        self.assertGreater(tarefa_id, 0)

    def test_listar_tarefas(self):
        inserir_usuario("testuser3", "senha789")
        user_id = pega_id("testuser3")

        inserir_tarefas("Tarefa A", user_id, 0)
        inserir_tarefas("Tarefa B", user_id, 1)

        tarefas = listar_tarefas(user_id)
        self.assertEqual(len(tarefas), 2)
        self.assertEqual(tarefas[0][1], "Tarefa A") # Descrição
        self.assertEqual(tarefas[0][2], 0)         # Status
        self.assertEqual(tarefas[1][1], "Tarefa B")
        self.assertEqual(tarefas[1][2], 1)

    def test_deletar_tarefa(self):
        inserir_usuario("testuser4", "senha101")
        user_id = pega_id("testuser4")
        tarefa_id = inserir_tarefas("Tarefa para deletar", user_id, 0)

        self.assertTrue(deletar_tarefa(tarefa_id)) # Deve retornar True se sucesso

        tarefas_restantes = listar_tarefas(user_id)
        self.assertEqual(len(tarefas_restantes), 0)

    def test_atualizar_status_tarefa(self):
        inserir_usuario("testuser5", "senha202")
        user_id = pega_id("testuser5")
        tarefa_id = inserir_tarefas("Tarefa para atualizar", user_id, 0)

        self.assertTrue(atualizar_checkbox(tarefa_id, 1)) # Atualiza para concluída

        tarefas = listar_tarefas(user_id)
        self.assertEqual(tarefas[0][2], 1) # Verifica se o status foi atualizado

if __name__ == '__main__':
    unittest.main()