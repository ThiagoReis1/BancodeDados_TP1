import os
from dashboard_funcs import *
def menu():
    print("╔═════════════════════════Central Super Banco═════════════════════════╗")
    print("║ Selecione uma opção (Opção 'x' finaliza o programa!):               ║")
    print("║                                                                     ║")
    print("║   a) Dado um produto:                                               ║")
    print("║      Liste as 5 avaliações mais úteis e com as maiores notas        ║")
    print("║      Liste as 5 avaliações mais úteis e com as menores notas        ║")
    print("║                                                                     ║")
    print("║   b) Dado um produto:                                               ║")
    print("║      Liste os produtos similares com vendas mais altas              ║")
    print("║                                                                     ║")
    print("║   c) Dado um produto:                                               ║")
    print("║      Mostre a evolução diária das médias de avaliação               ║")
    print("║      durante o intervalo de tempo desejado                          ║")
    print("║                                                                     ║")
    print("║   d) Liste os 10 produtos mais vendidos em cada grupo de produto    ║")
    print("║                                                                     ║")
    print("║   e) Liste os 10 produtos com a média mais alta de avaliações       ║")
    print("║      positivas úteis por produto                                    ║")
    print("║                                                                     ║")
    print("║   f) Liste as 5 principais categorias de produtos com a média       ║")
    print("║      mais alta de avaliações positivas úteis por produto            ║")
    print("║                                                                     ║")
    print("║   g) Liste os 10 clientes principais que fizeram mais comentários   ║")
    print("║      por grupo de produto                                           ║")
    print("║                                                                     ║")
    print("║   x) Sair                                                           ║")
    print("║                                                                     ║")
    print("╚═════════════════════════════════════════════════════════════════════╝")

def r_para_retorna(entrada): 
    if entrada == 'r':
        return True

def interface():
    indc = invalido = False
    while (not indc):
        menu()
        if invalido:
            print('Comando inválido!')
        indc, invalido = menu_opcoes(input())
        os.system('cls' if os.name == 'nt' else 'clear')

def menu_opcoes(entrada):
    if entrada == 'a':
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            entrada = input('Digite o código ASIN de um produto (r para voltar): ')
            
            if r_para_retorna(entrada):
                return False, False
            
            if verificar_produto_existe(entrada):
                top_reviews(entrada)
                input("Pressione Enter para continuar...")
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                print("Produto não encontrado (Verifique se o código tá correto)!")

    elif entrada == 'b':
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            entrada = input('Digite o código ASIN de um produto (r para voltar): ')
        
            if r_para_retorna(entrada):
                return False, False
            
            if verificar_produto_existe(entrada):
                produtos_similares(entrada)
                input("Pressione Enter para continuar...")
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                print("Produto não encontrado (Verifique se o código tá correto)!")

    elif entrada == 'c':
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            entrada = input('Digite o código ASIN de um produto (r para voltar): ')
            if r_para_retorna(entrada):
                return False, False

            n = int(input('Digite o número de dias que deseja analisar: '))
            
            if verificar_produto_existe(entrada):
                evolucao_dia_aval(entrada,n)
                input("Pressione Enter para continuar...")
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                print("Produto não encontrado (Verifique se o código tá correto)!")

    elif entrada == 'd':
        os.system('cls' if os.name == 'nt' else 'clear')

        dez_topV_grupo()

        input("Pressione Enter para continuar...")
        return False, False

    elif entrada == 'e':
        os.system('cls' if os.name == 'nt' else 'clear')

        produtos_mais_util()

        input("Pressione Enter para continuar...")
        return False, False
    elif entrada == 'f':
        os.system('cls' if os.name == 'nt' else 'clear')

        categorias_mais_util()

        input("Pressione Enter para continuar...")
        return False, False
    elif entrada == 'g':
        os.system('cls' if os.name == 'nt' else 'clear')

        melhores_comentarios_grupo()

        input("Pressione Enter para continuar...")
        return False, False
    elif entrada == 'x':
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Encerrando Programa')
        return True, False
    else:
        return False, True


