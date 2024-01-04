from adiciona import *
import re

def ler_linha(arquivo, n_cat):
    for i in range(n_cat):
        linha = arquivo.readline()
        if not linha:
            break
        yield linha

def ler_arquivo(nome_arq):
    try:
        with open(nome_arq, 'r',encoding='utf8') as file:
            
            produtos = []
            produto = {}
            for linha in file:
                print(linha)
                if 'discontinued' in linha:
                    produtos.append(produto)
                    produto = {}
                    continue
                match = re.search(r"ASIN:\s*(.*)", linha)
                if match:
                    produto['asin'] = match.group(1).strip()
                    continue
                match = re.search(r"title:\s*(.*)", linha)
                if match:
                    produto['title'] = match.group(1).strip()
                    continue
                match = re.search(r"group:\s*(.*)", linha)
                if match:
                    produto['product_group'] = match.group(1).strip()
                match = re.search(r"salesrank:\s*(.*)", linha)
                if match:
                    produto['sales_rank'] = match.group(1).strip()
                    continue
                if 'similar' in linha:
                    produto['similar'] = [x.strip() for x in linha.split()[2:]]
                        
                if 'categories' in linha:
                    categorias = []
                    n_cat = int(linha.split()[1])
                    for cat_linha in ler_linha(file, n_cat):

                        resultado = re.findall(r"\|(.*?)\[(\d+)\]", cat_linha)
                        categorias.append(resultado)

                    
                    resultados = [[item[0], item[1]] for sublist in categorias for item in sublist]
                    produto['categories'] = resultados
                
                if "reviews" in linha:
                    aux = []
                    reviews = re.findall(r'(\d{4}-\d{1,2}-\d{1,2})\s+cutomer:\s+(\w+)\s+rating:\s+(\d+)\s+votes:\s+(\d+)\s+helpful:\s+(\d+)', file.readline())
                    while reviews:
                        aux.append(reviews)
                        reviews = re.findall(r'(\d{4}-\d{1,2}-\d{1,2})\s+cutomer:\s+(\w+)\s+rating:\s+(\d+)\s+votes:\s+(\d+)\s+helpful:\s+(\d+)', file.readline())
                    if len(aux) > 0:
                        produto['reviews'] = aux
                    produtos.append(produto)
                    produto = {}

            print("Leitura do arquivo finalizado!")
            return produtos
            
    except FileNotFoundError as e:
        print(f"O arquivo não foi encontrado: {e}")
    except ValueError as e:
       print(f"O valor é inválido no arquivo lido: {e}")
    except IndexError as e:
        print(f"Ocorreu um erro de índice: {e}")
    except Exception as e:
        print(f"Erro: {e}")