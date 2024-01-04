import iniciar
import criar_tabelas
from adiciona import BD_adicionar_produtos
from leitura import ler_arquivo


if __name__ == '__main__':
    
    
    iniciar.criar_BD()
    criar_tabelas.criar_tabelas()

    filename = 'amazon-meta-sample.txt'
    products = ler_arquivo(filename)
    BD_adicionar_produtos(products)



    
