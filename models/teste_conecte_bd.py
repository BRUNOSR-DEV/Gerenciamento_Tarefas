
import unittest
import os
import MySQLdb

from models.conecte_bd import (
    conectar, desconectar, inserir_usuario,
    inserir_tarefas, pega_id, listar_tarefas, deletar_tarefa,
    atualizar_checkbox, pega_dados
)

