from util.banco_de_dados import Database
import datetime
import bcrypt
import os



class Interface():
    def __init__(self):
        self.bd = Database('root', '99227512Biel*', 'localhost', 'projeto') #12345678

    def cadastrar_usuario(self, nome, nasci, email, senha):
        consulta = self.bd.consultar_usuario(email)
        if len(consulta)==0: #validar
            self.bd.cadastrar_usuario(nome, email, self.critografar(senha), nasci)
            return self.bd.consultar_usuario(email)[0]
        return False

    def criar_sessao(self, ip, usuario):
        hora_acesso = datetime.datetime.now()
        self.bd.cadastrar_sessao(ip, hora_acesso, usuario)
    
    def sessao_valida(self, ip, usuario):
        consulta = self.bd.consultar_sessao(ip, usuario)[0] #[id_sessao, ip, ultimo_acesso, usuario]
        if consulta==1 and consulta[1]==ip and consulta[3]==usuario:
            hora_acesso = datetime.datetime.now()
            if (consulta[2] - hora_acesso).total_seconds() < 3600: # verificar se não passou 1h
                self.bd.atualizar_sessao(consulta[0], hora_acesso)
                return True
            self.bd.remover_sessao(ip, usuario)
        return False
    
    def login(self, email, senha, ip):
        consulta = self.bd.consultar_usuario(email) #[id, nome, email, senha, nasci]
        if consulta!=[] and consulta[0][2]==email and self.comparar_senha(senha, consulta[0][3]): #adicionar validador
            self.criar_sessao(ip, consulta[0][0])
            return consulta[0][0]
        return False

    def logout(self, ip, usuario):
        try:
            self.bd.remover_sessao(ip, usuario)
            return True
        except:
            return False

    def critografar(self, senha):#pip install bcrypt
        return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt(10))
    
    def comparar_senha(self, senha1, senha2):
        return bcrypt.checkpw(senha1.encode('utf-8'), senha2.encode('utf-8'))

    def cadastrar_produto(self, nome, descricao, ficha_tecnica, valor, estoque, imagem, vendedor):
        if self.arquivo_permitido(imagem.filename):
            self.bd.cadastrar_produto(nome, descricao, ficha_tecnica, valor, estoque, vendedor)
            id_produto = self.bd.consultar_produto(vendedor)[-1][0]
            nome_imagem = str(vendedor)+"--"+str(id_produto)+"--"+str(datetime.datetime.now()).replace(" ","")+'.'+imagem.filename.rsplit('.', 1)[1].lower()
            print("cumprimento nome_imagem: ", len(nome_imagem))
            imagem.save(os.path.join('static/imagens_produtos', nome_imagem))
            self.bd.cadastrar_imagem(nome_imagem, id_produto)
            return True

        return False
 
    def arquivo_permitido(self, filename):
        extensoes_permitidas = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensoes_permitidas

    def cadastrar_endereco(self, cep, estado, cidade, bairro, rua, numero, complemento, id_usuario):
        self.bd.cadastrar_endereco(estado, cidade, bairro, rua, numero, cep, id_usuario)

    def consultar_endereco(self, id_usuario):
        return self.bd.consultar_endereco(id_usuario)
    
    def cadastrar_cartao(self, numero, nome, cpf, vencimento, cvv, usuario):
        self.bd.cadastrar_cartao(numero, nome, cpf, vencimento, cvv, usuario)

    def consultar_cartao(self, id_usuario):
        consulta = self.bd.consultar_cartao(id_usuario)
        for i in range(len(consulta)):
            consulta[i] = list(consulta[i])
            consulta[i][1] = 'XXXX XXXX XXXX '+consulta[i][1][-4:]
        # tratamento para html
    
    def cadastrar_compra(self, quantidade, valor, id_usuario, id_cartao, id_endereco, id_produto):
        self.bd.cadastrar_compra(quantidade, quantidade*valor, id_usuario, id_cartao, id_endereco, id_produto)

    def consultar_compras(self, id_usuario):
        # tratamento para html
        return self.bd.cadastrar_compras(id_usuario)
