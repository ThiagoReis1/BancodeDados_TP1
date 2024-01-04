import psycopg2
from a_COMECE_AQUI import obter_config_postgres

def apagar_BD():
    conn = None
    try:
        
        conn = psycopg2.connect(**obter_config_postgres())
        conn.autocommit = True  

        
        cur = conn.cursor()

        
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'bancodedados'")
        existe = cur.fetchone()

        if existe:
            
            cur.execute("DROP DATABASE bancodedados")
            print("O banco de dados foi apagado")
        else:
            print("O banco de dados não foi criado ou já foi apagado")

        
        cur.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

apagar_BD()