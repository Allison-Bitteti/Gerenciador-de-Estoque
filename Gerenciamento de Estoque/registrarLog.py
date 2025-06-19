from datetime import datetime

class RegistrarLog:
    @staticmethod
    def registrarAtividades(mensagem: str):
        with open(r"Arquivos/atividades.log", "a", encoding="utf-8") as log:
            momento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log.write(f'[{momento}] {mensagem.strip().upper()}\n')
