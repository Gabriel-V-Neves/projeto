from banco_de_dados import Database
import datetime


class Interface():
    def __init__(self):
        self.bd = Database('root', '99227512Biel*', 'localhost', 'projeto')

    def cadastrar_usuário(self, dados_usuario):
        try:
            if True: #validar
                self.bd.criar_usuario(*dados_usuario)
                return True
        except:
            return False
    
    def sessao_valida(self, ip, usuario):
        consulta = self.bd.consultar_sessao(ip, usuario) #[id_sessao, ip, ultimo_acesso, usuario]
        if consulta==1 and consulta[1]==ip and consulta[3]==usuario:
            hora_acesso = datetime.datetime.now()
            if (consulta[2] - hora_acesso).total_seconds() < 3600: # verificar se não passou 1h
                self.bd.atualizar_sessao(consulta[0], hora_acesso)
                return True
            self.bd.remover_sessao(ip, usuario)
        return False

    
    def login(self, email, senha, ip):
        consulta = self.bd.consultar_usuario() #[id, nome, email, senha, nasci]
        if consulta==1 and consulta[2]==email and consulta[3]==senha: #adicionar validador
            self.db.criar_sessao(consulta[0], ip)
            return consulta[1]
        return False

    def logout(self, ip, usuario):
        try:
            self.bd.remover_sessao(ip, usuario)
            return True
        return False
