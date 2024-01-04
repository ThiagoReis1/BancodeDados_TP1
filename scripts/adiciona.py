import psycopg2
from psycopg2.extras import execute_values
from a_COMECE_AQUI import obter_config_bd


def BD_adicionar_produtos(produto_dics):
    
    inserir_produto = "INSERT INTO produto(asin,titulo,grupo,vendas) VALUES %s RETURNING asin;"
    
    inserir_assin_similares = "INSERT INTO produtos_similar(asin_similar,asin_produto) VALUES %s "
    
    inserir_review = "INSERT INTO review(asin_produto,data,cliente,aval,voto,util) VALUES %s"
    
    inserir_categoria_info = "INSERT INTO categoria_info(categoria_id,nome) VALUES %s ON CONFLICT DO NOTHING"
    
    inserir_categoria = "INSERT INTO categoria(asin_produto,categoria_id) VALUES %s"
    
    conn = None
    try:
        
        conn = psycopg2.connect(**obter_config_bd())
        conn.autocommit = False  
        cur = conn.cursor()

        
        cur.execute("BEGIN")

        
        produtos = [(produto_dic['asin'], produto_dic['title'], produto_dic['product_group'], produto_dic['sales_rank']) for produto_dic in produto_dics if len(produto_dic) > 1]
        execute_values(cur,  inserir_produto , produtos, page_size=10000)

        
        cur.execute("SELECT asin FROM produto")
        linhas_produto_BD = cur.fetchall()
        
        if linhas_produto_BD:
            for i, row in enumerate(linhas_produto_BD):
                produto_dic = produto_dics[i]
                asin_produto = produto_dic['asin']

                
                if 'similar' in produto_dic:
                    produtos_similar = produto_dic['similar']
                    if produtos_similar:
                        valores_similares = [(asin_similar, asin_produto) for asin_similar in produtos_similar]
                        execute_values(cur, inserir_assin_similares, valores_similares, page_size=1000)

                
                if 'categories' in produto_dic:
                    categories = produto_dic['categories']
                    if categories:
                        categorias_info = list(set([(categoria[1], categoria[0]) for categoria in categories]))
                        execute_values(cur,inserir_categoria_info,categorias_info, page_size=1000)
                        categoria_values = list(set([(asin_produto, categoria[-1]) for categoria in categories]))
                        execute_values(cur, inserir_categoria, categoria_values, page_size=1000)

                
                if 'reviews' in produto_dic:
                    reviews = produto_dic['reviews']
                    if reviews:
                        rev = [(asin_produto, *review[0][:5]) for review in reviews]
                        execute_values(cur, inserir_review, rev, page_size=1000)
        
        conn.commit()
        print("Dados inseridos no Banco de Dados!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()  
    finally:
        if conn is not None:
            conn.close()