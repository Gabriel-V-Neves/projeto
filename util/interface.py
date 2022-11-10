from banco_de_dados import Database


class Interface():
    def __init__(self):
        self.bd = Database('root', '99227512Biel*', 'localhost', 'projeto')

    def cadastrar_usuário(self, dados_usuario):
        if True: #validar
            self.bd.criar_usuario(*dados_usuario)
            return True
        return False
    
    def login(self, email, senha):
        if True: #validar
            # criar função email
            return True
        return False