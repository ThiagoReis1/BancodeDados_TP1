import psycopg2




def criar_BD():

    conn = None
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='1234', host='localhost')

    conn.autocommit = True  
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'bancodedados'")

    if not cur.fetchone(): #se o banco não esta criado, então crie
        cur.execute("CREATE DATABASE bancodedados")

    cur.close()
    conn.close()

    print("Banco de Dados Criado")
  
