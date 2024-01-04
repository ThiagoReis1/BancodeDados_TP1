import psycopg2
from a_COMECE_AQUI import obter_config_postgres




def criar_BD():

    conn = None
    conn = psycopg2.connect(**obter_config_postgres())

    conn.autocommit = True  
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'bancodedados'")

    if not cur.fetchone(): #se o banco não esta criado, então crie
        cur.execute("CREATE DATABASE bancodedados")

    cur.close()
    conn.close()

    print("Banco de Dados Criado")
  
