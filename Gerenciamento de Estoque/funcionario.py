import hashlib
import csv
import os
from time import sleep

from registrarLog import RegistrarLog

class Funcionario(RegistrarLog):
    def __init__(self):
        self.usuarios_arquivo = r"Arquivos/usuarios.csv"
    
    # Codifica a senha
    @staticmethod
    def gerar_hash(senha: str) -> str:
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def cadastrarFuncionario(self, usuario: str):
        os.system('cls')

        print('Insira as seguintes informacoes:')
        nomeFuncionario = input("Nome: ").strip().replace(' ', '_').upper()

        senha = input('Senha: ').strip()
        senha = self.gerar_hash(senha)

        if usuario == "SISTEMA":
            nivel = 1
            with open(self.usuarios_arquivo, 'w', encoding="utf-8") as arquivo:
                arquivo.write("NOME;SENHA;NÍVEL\n")
        else:
            while True:
                try:
                    nivel = int(input('Nível de Autorização: '))
                except ValueError:
                    print("Erro no Nível de Autorização!!!")
                else:
                    break
        
        if self.funcionariExiste(nomeFuncionario):
            print("Funcionário já existe!!!")
            sleep(2)
            return # Volta ao menu
        
        with open(self.usuarios_arquivo, 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'{nomeFuncionario};{senha};{nivel}\n')
            print("Funcionário Cadastrado Com Sucesso!")
            self.registrarAtividades(f"{usuario} cadastrou o funcionário {nomeFuncionario}")
            sleep(2)
            return
        
    def funcionariExiste(self, funcionario: str):
        with open(self.usuarios_arquivo, 'r', newline='', encoding="utf-8") as arquivo:
            leitor = csv.reader(arquivo, delimiter=";")
            for linha in leitor:
                if linha[0] == funcionario:
                    return True
        return False