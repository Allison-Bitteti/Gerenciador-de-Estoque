import csv
import os
from time import sleep

from produto import Produto
from funcionario import Funcionario
from registrarLog import RegistrarLog

class Main(Produto, Funcionario):
    def __init__(self, usuario, senha, nivel):
        Funcionario.__init__(self)
        self.usuario = usuario
        self.senha = senha
        self.nivel = int(nivel)
        
    def sair(self):
        os.system('cls')
        print("Programa Finalizado")
        RegistrarLog.registrarAtividades(f"Usuário {self.usuario} saiu do sistema")
        return "logout" # Retorna ao login
    
    def menu(self):
        opcoes = {
            1: 'Cadastrar Produto',
            2: 'Atualizar Produto', 
            3: 'Deletar Produto', 
            4: 'Visualizar Estoque',
            5: 'Cadastrar Funcionário',
            6: 'Sair do Sistema',
        }
        
        opcoes_nivel1 = [1, 2, 3, 4, 5, 6]
        opcoes_nivel2 = [4, 6]
        
        acoes_nivel1  = {
            1: lambda: self.cadastrar(self.usuario),
            2: lambda: self.atualizar(self.usuario),
            3: lambda: self.deletar(self.usuario),
            4: lambda: self.visualizarEstoque(),
            5: lambda: self.cadastrarFuncionario(self.usuario),
            6: lambda: self.sair(),
        }
        
        acoes_nivel2  = {
            1: lambda: self.visualizarEstoque(),
            2: lambda: self.sair(),
        }
        
        opcoes_ativas = opcoes_nivel1 if self.nivel == 1 else opcoes_nivel2
        acoes_ativas = acoes_nivel1 if self.nivel == 1 else acoes_nivel2
        
        while True:
            os.system('cls') # Limpa o Terminal

            print(f"Bem Vindo {self.usuario} ao Sistema da Loja =)")
            
            contador = 1
            for opcao in opcoes_ativas:
                print(f'[{contador}] {opcoes[opcao]}')
                contador += 1
                    
            print("O que deseja fazer?")
            
            try:
                opcao = int(input('> '))
            except ValueError:
                print("Opção Inválida!!!")
                sleep(2)
                continue

            resultado = acoes_ativas.get(opcao, lambda: print("Opção Inválida!!!"))()
            
            if resultado == "logout":
                return "logout"

try:
    os.mkdir("Arquivos")
except:
    pass

usuarios_arquivo = r'Arquivos/usuarios.csv'

if not os.path.exists(usuarios_arquivo) or os.stat(usuarios_arquivo).st_size == 0:
    print("Primeiro acesso ao sistema")
    print("Iniciando Cadastro do Administrador...")
    sleep(2)
    
    funcionario = Funcionario()
    funcionario.cadastrarFuncionario("SISTEMA")
else:              
    while True:
        os.system('cls')
        
        usuario = input('Usuário: ').upper()
        senha = input('Senha: ')
        autentificacao = False  
        
        senha_hash = Funcionario.gerar_hash(senha=senha)
        
        with open(r'Arquivos/usuarios.csv', 'r', newline='', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo, delimiter=";")
            for linha in leitor:
                usuario_arquivo = linha[0]
                senha_arquivo = linha[1]

                if usuario_arquivo == usuario and senha_arquivo == senha_hash:
                    nivel = linha[2]
                    
                    autentificacao = True
                    break

        if autentificacao:
            RegistrarLog.registrarAtividades(f"Usuário {usuario} fez login")
            main = Main(usuario, senha, nivel)
            resultado = main.menu()
            
            if resultado == "logout":
                continue
                        
        else:
            RegistrarLog.registrarAtividades(f'Tentativa de login do usuário {usuario}')
            print('Usuário ou Senha Inválidos!!!')
            sleep(2)