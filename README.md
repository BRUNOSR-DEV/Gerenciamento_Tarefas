# 📝 Gerenciador de Tarefas (Desktop App)
Aplicação desktop para gerenciamento de tarefas, desenvolvida para demonstrar proficiência em Engenharia de Software, Modelagem de Dados Relacional e interfaces gráficas modernas com Python.

# 🏗️ Arquitetura e Modelagem (MER)
Diferente de scripts simples, este projeto foi precedido por uma etapa de design de banco de dados.

Modelo Entidade-Relacionamento: Localizado na pasta modelo_ER/, o projeto conta com um diagrama (.mwb e .png) que define as relações entre usuários e tarefas.

Normalização: Estrutura planejada para garantir a integridade referencial e performance nas consultas MySQL.

# 🚀 Funcionalidades Principais
Sistema de Login & Cadastro: Fluxo completo de autenticação de usuários.

Gestão Dinâmica de Tasks: Operações de CRUD (Criar, Ler, Atualizar e Deletar) vinculadas em tempo real ao MySQL.

Interface Dark Mode: Desenvolvida com customtkinter para uma experiência de usuário (UX) moderna e fluida.

Robustez de Conexão: Implementação de tratamento de erros e logs para falhas de banco de dados.

# 🛠 Tecnologias e Bibliotecas
Core: Python 3.11

UI/UX: CustomTkinter

Database: MySQL 8.0

Connector: mysql-connector-python

DevOps/Infra: configparser (para gestão de credenciais via config.ini) e venv.

# 📁 Destaques da Estrutura
gerenciador.py: Ponto de entrada e controlador da interface.

models/conecte_bd.py: Camada de persistência (Data Access Object).

teste_conecte_bd.py: Script de Diagnóstico independente para validar a saúde da conexão com o banco de dados antes da execução do sistema.

utils/helper.py: Funções utilitárias reutilizáveis para lógica de apoio.

# 🔧 Instalação e Testes
Clone o repositório:

Bash

git clone https://github.com/BRUNOSR-DEV/GERENCIADOR_TAREFAS.git
Prepare o Ambiente:

Bash

.\vir_gt\Scripts\activate
pip install customtkinter mysql-connector-python
Validação de Infraestrutura:
Antes de iniciar o app, rode o script de teste para garantir que suas credenciais no config.ini.example estão corretas:

Bash

python teste_conecte_bd.py
Execução:

Bash

python gerenciador.py