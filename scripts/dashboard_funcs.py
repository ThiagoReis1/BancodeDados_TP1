import psycopg2

import datetime



def evolucao_dia_aval(asin, n):
    try:
        
        conn = psycopg2.connect(dbname='bancodedados', user='postgres', password='1234', host='localhost')
        cur = conn.cursor()

        cur.execute("""
            SELECT date_trunc('day', data) AS review_date, AVG(aval) AS avg_rating
            FROM review
            WHERE asin_produto = %s
            GROUP BY review_date
            ORDER BY review_date
            LIMIT %s
        """, (asin, n,))

        linhas = cur.fetchall()
        print_linha()
        print(f"Esta é a evolução diária das medias de avaliação do produto com asin = {asin} em {n} dia(s):\n")
        for day in linhas:
            data = day[0]
            
            data_formatada = data.strftime('%Y-%m-%d')

            print(f'data: {data_formatada}   media de avaliação: {day[1]:.2f}')

        print_linha()
        cur.close()
        conn.commit()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()


def dez_topV_grupo():
    try:
        
        conn = psycopg2.connect(dbname='bancodedados', user='postgres', password='1234', host='localhost')
        cur = conn.cursor()

        cur.execute("SELECT DISTINCT grupo FROM produto")
        linhas = cur.fetchall()

        for grupo in linhas:
            print_linha()
            print(f'grupo: {grupo[0]}')
            print()
            cur.execute("""
                SELECT produto.titulo, produto.vendas
                FROM produto
                WHERE produto.grupo = %s AND produto.vendas >= 1
                ORDER BY produto.vendas
                LIMIT 10;
            """, (grupo,))

            linhas = cur.fetchall()
            for produto in linhas:
                print(f'Título: {produto[0]}')
                print(f'vendas: {produto[1]}')
                print_linha()

        print("Os 10 produtos líderes de venda em cada grupo de produtos!")
        print("OBS: Caso tenha menos de 10 produtos,então o grupo menos de 10 produtos cadastrados!")
        cur.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def produtos_mais_util():
    try:
        
        conn = psycopg2.connect(dbname='bancodedados', user='postgres', password='1234', host='localhost')
        cur = conn.cursor()

        cur.execute("""
            SELECT p.asin, p.titulo, AVG(r.util) as avg_helpful
            FROM produto p
            JOIN review r ON p.asin = r.asin_produto
            GROUP BY p.asin, p.titulo
            ORDER BY avg_helpful DESC
            LIMIT 10;
        """)

        linhas = cur.fetchall()
        print_linha()
        cont = 1
        for produto in linhas:
            print(f'Top {cont}:')
            print(f'ASIN: {produto[0]}')
            print(f'Título: {produto[1]}')
            print(f'media de avaliações Úteis: {produto[2]:.2f}')
            print_linha()
            cont += 1
        print("Os 10 produtos com a maior media de avaliações úteis positivas por produto!")
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



def categorias_mais_util():
    try:
        
        conn = psycopg2.connect(dbname='bancodedados', user='postgres', password='1234', host='localhost')
        cur = conn.cursor()

        cur.execute("""
            SELECT ci.categoria_id, AVG(r.util) as avg_helpful
            FROM categoria c
            JOIN produto p ON c.asin_produto = p.asin
            JOIN review r ON r.asin_produto = p.asin
            JOIN categoria_info ci ON c.categoria_id = ci.categoria_id
            WHERE r.util > 0
            GROUP BY ci.categoria_id
            ORDER BY avg_helpful DESC
            LIMIT 5;
        """)
        linhas = cur.fetchall()

        print_linha()
        cont = 1
        for linha in linhas:
            print_linha()
            print(f'Top {cont}')
            print(f"categoria: {linha[0]}\nMédia de avaliações Úteis: {linha[1]:.2f}")
            cont += 1
        print("\nAs 5 categorias de produto com a maior média de avaliações úteis positivas por produto!")
        print_linha()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


def melhores_comentarios_grupo():
    
    conn = psycopg2.connect(dbname='bancodedados', user='postgres', password='1234', host='localhost')
    cur = conn.cursor()

    try:
        cur.execute("SELECT DISTINCT grupo FROM produto")
        linhas = cur.fetchall()

        print_linha()
        for grupo in linhas:
            print(f'grupo: {grupo[0]}\n')
            cont = 1
            cur.execute("""
                SELECT cliente, COUNT(*) AS total_comments
                FROM review
                INNER JOIN produto ON review.asin_produto = produto.asin
                WHERE grupo = %s
                GROUP BY cliente
                ORDER BY total_comments DESC
                LIMIT 10
            """, (grupo[0],))
            
            linhas = cur.fetchall()
           
            for usuario in linhas:
                print(f'Top {cont}:')
                print(f'cliente: {usuario[0]}')
                print(f'Total de Comentários: {usuario[1]}')
                print_linha()
                cont += 1
            print()
        
        print("os 10 clientes que mais fizeram comentários por grupo de produto!")
        print("OBS: Se for menos de 10 clientes, então o grupo tem menos que 10 clientes !")
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

def print_linha():
    print("-------------------------------------------------")


def verificar_produto_existe(asin):
    
    conn = psycopg2.connect(dbname='bancodedados', user='postgres', password='1234', host='localhost')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM produto WHERE asin = %s", (asin,))
    existe = cursor.fetchone()[0] > 0
    cursor.close()
    return existe


def top_reviews(asin):
    
    conn = psycopg2.connect(dbname='bancodedados', user='postgres', password='1234', host='localhost')
    cur = conn.cursor()

    
    sql_func1 = f"""
        SELECT * FROM (
            SELECT ROW_NUMBER() OVER (ORDER BY aval DESC, util DESC) AS top,
                cliente, data, aval, voto, util
            FROM review
            WHERE asin_produto = '{asin}'
        ) AS top_reviews
        WHERE top <= 5
    """

    
    sql_func2 = f"""
        SELECT * FROM (
            SELECT ROW_NUMBER() OVER (ORDER BY aval ASC, util DESC) AS top,
                cliente, data, aval, voto, util
            FROM review
            WHERE asin_produto = '{asin}'
        ) AS top_reviews
        WHERE top <= 5
    """

    try:
        print_linha()
        print("Os 5 comentários mais úteis e com maior avaliação:")
        print("(top,cliente,data,aval,votes,util)\n")
        cur.execute(sql_func1)
        linhas = cur.fetchall()

        for linha in linhas:
            print(linha)
        print_linha()

        print("Os 5 comentários mais úteis e com menor avaliação:")
        print("(top,cliente,data,aval,votes,util)\n")

        cur.execute(sql_func2)
        linhas = cur.fetchall()

        for linha in linhas:
            print(linha)

        print_linha()

    except Exception as e:
        print(f"Ocorreu um erro ao consulta o Banco de Dados: {e}")
    finally:
        cur.close()
        conn.close()


def produtos_similares(asin):
    try:
        
        conn = psycopg2.connect(dbname='bancodedados', user='postgres', password='1234', host='localhost')
        cur = conn.cursor()
        cur.execute(f"""SELECT sp.asin_similar, p.titulo, p.vendas as sales_rank_similar
                        FROM produtos_similar sp
                        JOIN produto p ON sp.asin_similar = p.asin
                        WHERE sp.asin_produto = '{asin}' AND p.vendas < (
                            SELECT vendas
                            FROM produto
                            WHERE asin = '{asin}'
                        )
                        ORDER BY p.vendas ASC
                        LIMIT 5""")
        linhas = cur.fetchall()
        cont = 1
        print_linha()
        
        if len(linhas) > 1:
            print(f"Digite o código ASIN do produto = {asin}, abaixo está a lista de produtos similares com maiores vendas do que ele:\n")
        else:
            print("Não tem produtos similares com números maiores de venda!")
        for produto in linhas:
            print(f'produto {cont}:\n')
            print(f'ASIN: {produto[0]}')
            print(f'Título: {produto[1]}')
            print(f'vendas: {produto[2]}')
            print_linha()
            cont += 1
    except Exception as error:
        print(f"Error: {error}")
    finally:
        cur.close()
        conn.close()
