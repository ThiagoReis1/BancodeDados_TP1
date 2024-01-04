import psycopg2
from a_COMECE_AQUI import obter_config_bd


def criar_tabelas():
    

    produto = """
        CREATE TABLE produto (
            asin varchar(15)  NOT NULL PRIMARY KEY,
            titulo varchar(500)  NOT NULL,
            grupo varchar(20)  NOT NULL,
            vendas int  NOT NULL
        )
    """

    review = """
        CREATE SEQUENCE review_id_seq
            START WITH 0
            INCREMENT BY 1
            MINVALUE 0
            NO MAXVALUE
            CACHE 1;
        CREATE TABLE review (
            id INTEGER DEFAULT NEXTVAL('review_id_seq'),
            asin_produto varchar(15)  NOT NULL,
            cliente varchar(20)  NOT NULL,
            data date  NOT NULL,
            aval int  NOT NULL,
            voto int  NOT NULL,
            util int  NOT NULL,
            CONSTRAINT review_pk PRIMARY KEY (id,asin_produto,cliente),
            FOREIGN KEY (asin_produto)
                REFERENCES produto (asin)
                ON DELETE CASCADE
                NOT DEFERRABLE 
                INITIALLY IMMEDIATE
        )
    """

    produtos_similar = """
        CREATE TABLE produtos_similar (
            asin_produto  varchar(15)  NOT NULL,
            asin_similar varchar(15),
            CONSTRAINT similar_products_pk PRIMARY KEY (asin_produto ,asin_similar),
            FOREIGN KEY (asin_produto )
                REFERENCES produto (asin)  
                ON DELETE CASCADE
                NOT DEFERRABLE 
                INITIALLY IMMEDIATE
        )
    """

    categoria_info = """
        CREATE TABLE categoria_info (
            categoria_id int  NOT NULL PRIMARY KEY,
            nome varchar(100)  NOT NULL 
        )
    """

    categoria = """
        CREATE TABLE categoria (
            asin_produto  varchar(15)  NOT NULL,
            categoria_id int  NOT NULL,
            CONSTRAINT categoria_pk PRIMARY KEY (asin_produto ,categoria_id),
            FOREIGN KEY (asin_produto)
                REFERENCES produto (asin)  
                ON DELETE CASCADE
                NOT DEFERRABLE 
                INITIALLY IMMEDIATE,
            FOREIGN KEY (categoria_id)
                REFERENCES categoria_info (categoria_id)  
                ON DELETE CASCADE
                NOT DEFERRABLE 
                INITIALLY IMMEDIATE
        )
    """
    


    conn = None
    try:

        conn = psycopg2.connect(**obter_config_bd())
        cur = conn.cursor()
        
        
        cur.execute(produto)
        cur.execute(review)
        cur.execute(produtos_similar)
        cur.execute(categoria_info)
        cur.execute(categoria)
        
        cur.close()
        
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            print("Banco de dados foi criado!")
            conn.close()