
import unittest
import os
import MySQLdb

from models.conecte_bd import (
    conectar_bd_original, desconectar, inserir_usuario,
    inserir_tarefas, pega_id, listar_tarefas, deletar_tarefa,
    atualizar_checkbox, pega_dados
)

def conectar_teste():
    """
    Função para conectar ao servidor
    """
    try:
        conn = MySQLdb.connect(
            db= 'teste_bd_gerenciador_tarefas',
            host= 'localhost',
            user= 'hey',
            passwd= 'boney',
            autocommit=True,
        )
        return conn

    except MySQLdb.Error as e:
        print(f'Erro na conexão ao MySql Server de TESTE  : {e}')
        raise


def limpar_tabelas(conn):
    """
    Limpa os dados das tabelas de teste.
    """
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tarefas")
        cursor.execute("DELETE FROM usuario")
        # Se você tem auto-incremento, pode querer resetar para 1
        # cursor.execute("ALTER TABLE usuarios AUTO_INCREMENT = 1")
        # cursor.execute("ALTER TABLE tarefas AUTO_INCREMENT = 1")
        conn.commit() # Commit das operações de limpeza
        print("Tabelas de teste limpas.")
    except MySQLdb.Error as e:
        print(f"Erro ao limpar tabelas de teste: {e}")
        conn.rollback()
        raise # Re-levanta para falhar o teste


class TestGerenciadorTarefas(unittest.TestCase):

    def __init__(self, methodName= 'runTest'):
        super().__init__(methodName)
        self.conn= conectar_teste()

    # Este método é executado ANTES de CADA teste
    def setUp(self):
        self.conn = conectar_teste()
        # Limpa as tabelas antes de cada teste para garantir um estado limpo
        limpar_tabelas(self.conn) 
        print(f"\n--- Configurando teste: {self._testMethodName} ---")

    # Este método é executado DEPOIS de CADA teste
    def tearDown(self):
        # Fecha a conexão de teste para CADA TESTE
        if self.conn:
            self.conn.close()
        print(f"--- Limpando após teste: {self._testMethodName} ---")
        # Não remova arquivos aqui para MySQL


    def test_inserir_usuario_e_pegar_id(self):
        # Testa se um usuário pode ser inserido e se seu ID pode ser recuperado
        self.assertTrue(inserir_usuario("testuser_unit", "senha123", self.conn))
        user_id = pega_id("testuser_unit", self.conn)
        self.assertIsNotNone(user_id)
        self.assertGreater(user_id, 0) # ID deve ser maior que 0


    def test_inserir_tarefas(self):
        inserir_usuario("testuser2", "senha456", self.conn)
        user_id = pega_id("testuser2", self.conn)
        self.assertIsNotNone(user_id)

        tarefa_id = inserir_tarefas("Comprar leite", user_id, 0, self.conn)
        self.assertIsNotNone(tarefa_id)
        self.assertGreater(tarefa_id, 0)

    def test_listar_tarefas(self):
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
        inserir_usuario("testuser4", "senha101", self.conn)
        user_id = pega_id("testuser4", self.conn)
        tarefa_id = inserir_tarefas("Tarefa para deletar", user_id, 0, self.conn)

        self.assertTrue(deletar_tarefa(tarefa_id, self.conn)) # Deve retornar True se sucesso

        tarefas_restantes = listar_tarefas(user_id, self.conn)
        self.assertEqual(len(tarefas_restantes), 0)

    def test_atualizar_status_tarefa(self):
        inserir_usuario("testuser5", "senha202", self.conn)
        user_id = pega_id("testuser5", self.conn)
        tarefa_id = inserir_tarefas("Tarefa para atualizar", user_id, 0, self.conn)

        self.assertTrue(atualizar_checkbox(tarefa_id, 1, self.conn)) # Atualiza para concluída

        tarefas = listar_tarefas(user_id, self.conn)
        self.assertEqual(tarefas[0][2], 1) # Verifica se o status foi atualizado

if __name__ == '__main__':
    unittest.main()