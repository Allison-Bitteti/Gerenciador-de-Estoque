import csv
import os
from time import sleep

from registrarLog import RegistrarLog

class Produto(RegistrarLog):
    nomeProduto = ''
    qtd = 0
    preco = 0
    item = 1
    
    # Arquivo para salvar os dados dos produtos
    estoqueCSV = r"Arquivos/estoque.csv"

    def carregar_estoque(self):
        conteudo = []
        
        with open(self.estoqueCSV, 'r', newline='', encoding='utf-8') as arquivo:
                leitor = csv.reader(arquivo, delimiter=";")
                for linha in leitor:
                    conteudo.append(linha)
        return conteudo    
    
    def cadastrar(self, usuario):
        while True:
            os.system('cls')
            
            print('Insira as informações abaixo:')
            self.nomeProduto = input('> Nome do Produto: ').upper().strip().replace(" ", "_")
            
            try:
                self.qtd = int(input('> Quantidade: '))
                self.preco = float(input('> Preço: '))
            except ValueError:
                print("Valor Inválido!!!")
                sleep(2)
                continue
            
            if os.path.exists(self.estoqueCSV): # Verifica se o arquivo existe
                self.item = 0

                with open(self.estoqueCSV, 'r', encoding="utf-8") as arquivo: # Abre o arquivo no modo leitura (reader)
                    for linhas in arquivo.readlines():
                        produtos = linhas.replace("\n", "").split(";")

                        if produtos[1] == self.nomeProduto:
                            print("Produto Já Cadastrado!!!")
                            self.registrarAtividades(f"{usuario} cadastrou o produto {self.nomeProduto}\n")
                            self.item = 0
                            sleep(2)
                            return
                        else:
                            try:
                                self.item = int(produtos[0]) + 1
                            except:
                                pass
            else:
                with open(self.estoqueCSV, 'w', encoding='utf-8') as arquivo:
                    arquivo.write("ITEM;PRODUTO;QUANTIDADE;PREÇO\n")
            
            with open(self.estoqueCSV, "a", encoding="utf-8") as arquivo: # Abre o arquivo no modo adicionar (append)
                arquivo.write(f'{self.item};{self.nomeProduto};{self.qtd};{self.preco:.2f}\n')
                print("Produto Cadastrado com Sucesso")
                self.registrarAtividades(f"{usuario} cadastrou o produto {self.nomeProduto}\n")
            
            continuar = input("Deseja Cadastrar Mais Produtos? [S/N] ").upper()[0]
            if continuar == "N":
                return
            
    def atualizar(self, usuario):        
        if os.path.exists(self.estoqueCSV):
            while True:
                os.system("cls")
                
                print('Insira as informações abaixo:')
                self.nomeProduto = input('> Nome do Produto: ').upper().strip().replace(" ", "_")
                
                try:
                    self.qtd = int(input('> Quantidade: '))
                    self.preco = float(input('> Preço: '))
                except ValueError:
                    print("Valor Inválido!!!")
                    sleep(2)
                    continue

                conteudo = self.carregar_estoque()
                existe = False
                        
                for produto in conteudo:
                    if produto[1] == self.nomeProduto:
                        existe = True
                
                if existe:
                    for i in range(0, len(conteudo)):
                        if conteudo[i][1] == self.nomeProduto:
                            self.item = conteudo[i][0]
                            conteudo[i] = [self.item, self.nomeProduto, self.qtd, self.preco]
                            print("Produto Atualizado com Sucesso!")
                            self.registrarAtividades(f"{usuario} atualizou o produto {self.nomeProduto}\n")
                else:
                    print("Produto Não Cadastrado!!!")
                
                with open(self.estoqueCSV, "w", encoding="utf-8") as arquivo: # Abre o arquivo em modo escrita (writer)
                    for produto in conteudo:
                        arquivo.write(f'{produto[0]};{produto[1]};{produto[2]};{produto[3]}\n')
                
                continuar = input('Deseja Atualizar Mais Um Produto? [S/N] ').upper()[0]
                if continuar == 'N':
                    return
        else:
            print("Nenhum Produto Cadastrado!!!")
            sleep(2)
        
    def deletar(self, usuario):
        if os.path.exists(self.estoqueCSV):
            while True:
                os.system('cls')
                
                self.nomeProduto = input("Insira o Nome do Produto: ").upper().strip().replace(" ", "_")
                conteudo = self.carregar_estoque()
                novoConteudo = []
                existe = False
                
                for produto in conteudo:
                    if produto[1] == self.nomeProduto:
                        existe = True
            
                if existe:
                    for i in range(0, len(conteudo)):
                        if conteudo[i][1] != self.nomeProduto:
                            novoConteudo.append(conteudo[i])
                    print("Produto Deletado!")
                    self.registrarAtividades(f"{usuario} deletou o produto {self.nomeProduto}\n")
                else:
                    print("Produto Não Encontrado!!!")
                        
                with open(self.estoqueCSV, 'w', newline='', encoding='utf-8') as arquivo:
                    for produto in novoConteudo:
                        arquivo.write(f'{produto[0]};{produto[1]};{produto[2]};{produto[3]}\n')
                        
                continuar = input("Deseja Deletar Mais Um Produto? [S/N] ").upper()[0]
                if continuar == 'N':
                    return
        else:
            print("Nenhum Produto Cadastrado!!!")
            sleep(2)
    
    def visualizarEstoque(self):
        if os.path.exists(self.estoqueCSV):
            os.system("cls")
            
            conteudo = self.carregar_estoque()
            cabecalho = f'{'ITEM':<6}{'PRODUTO':<100}{'QUANTIDADE':<15}{'PREÇO':<10}'
            
            for produto in conteudo:
                print(f'{produto[0]:^6}{produto[1].replace("_", " "):<100}{produto[2]:<15}{produto[3]:<10}')
            
            while True:
                existe = False
                
                print('''[1] Mostrar Produto Específico
[2] Voltar pro Menu''')
                opcao = int(input("> "))
                
                if opcao == 1:
                    self.nomeProduto = input("Nome do Produto: ").upper().strip().replace(" ", "_")
                    
                    for produto in conteudo:
                        if produto[1] == self.nomeProduto:
                            existe = True
                    
                    if existe:
                        for produto in conteudo:                            
                            if produto[1] == self.nomeProduto:
                                print(cabecalho)
                                print(f'{produto[0]:^6}{produto[1].replace("_", " "):<100}{produto[2]:<15}{produto[3]:<10}')
                    else:
                        print('Produto Não Encontrado!!!')
                    
                elif opcao == 2:
                    return
                
                else:
                    print('Opção Inválida!!!')
        else:
            print('Nenhum Item Cadastrado!!!')
            sleep(2)