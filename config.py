"""Configurações de conexão com o banco de dados.

As variáveis podem ser sobrescritas via variáveis de ambiente.
"""

import os

MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", " ")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "db_produtos")
MYSQL_AUTOCOMMIT = False
