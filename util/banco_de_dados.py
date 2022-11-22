import mysql.connector
#from datetime import date, datetime


class Database():
    def __init__(self, user, password, host, database):
        self.cnx = mysql.connector.connect(user=user,
                                           password=password,
                                           host=host,
                                           database=database)

    def executar(self, comando, parametros):
        cs = self.cnx.cursor()
        cs.execute(comando, parametros)
        self.cnx.commit()
        cs.close()

    def consultar(self, comando, parametros):
        cs = self.cnx.cursor()
        cs.execute(comando, parametros)
        result = []
        for i in cs:
            result.append(i)
        return result

    def __del__(self):
        self.cnx.close()

    def criar_tabelas(self):
        sql = ["""
            create table if not exists usuario(
                id_usuario int auto_increment primary key,
                nome varchar(50),
                email varchar(50),
                senha varchar(60),
                nasci date
            )"""
            ,
            """
            create table if not exists sessao(
                id_sessao int auto_increment primary key,
                ip varchar(32),
                ultimo_acesso datetime,
                usuario int,
                constraint fk_usuariosessao foreign key (usuario)
                    references usuario(id_usuario)
            )"""
            ,
            """
            create table if not exists cartao(
                id_cartao int auto_increment primary key,
                numero varchar(16),
                nome varchar(50),
                cpf varchar(11),
                vencimento date,
                cvv int,
                usuario int,
                constraint fk_usuariocartao foreign key (usuario)
                    references usuario(id_usuario)
            )"""
            ,
            """
            create table if not exists endereco(
                id_endereco int auto_increment primary key,
                estado varchar(50),
                cidade varchar(50),
                bairro varchar(50),
                rua varchar(50),
                numero varchar(50),
                cep varchar(8),
                usuario int,
                constraint fk_usuarioendereco foreign key (usuario)
                    references usuario(id_usuario)
            )"""
            ,
            """
            create table if not exists produto(
                id_produto int auto_increment primary key,
                nome varchar(50),
                descricao varchar(500),
                ficha_tecnica varchar(500),
                valor decimal(6,2),
                estoque int,
                vendedor int,
                constraint fk_vendedorproduto foreign key (vendedor)
                    references usuario(id_usuario)
            )"""
            ,
            """
            create table if not exists imagem(
                id_imagem int auto_increment primary key,
                diretorio varchar(50),
                produto int,
                constraint fk_produtoimagem foreign key (produto)
                    references produto(id_produto)
            )""" 
            ,
            """
            create table if not exists compra(
                id_compra int auto_increment primary key,
                quantidade int,
                total decimal(6,2),
                usuario int,
                cartao int,
                endereco int,
                produto int,
                constraint fk_usuariocompra foreign key (usuario)
                    references usuario(id_usuario),
                constraint fk_cartaocompra foreign key (cartao)
                    references cartao(id_cartao),
                constraint fk_enderecocompra foreign key (endereco)
                    references endereco(id_endereco),
                constraint fk_produtocompra foreign key (produto)
                    references produto(id_produto)
            )"""
            ,
            """
            create table if not exists avaliacao(
                id_avaliacao int auto_increment primary key,
                nota decimal(2,1),
                descricao varchar(250),
                usuario int,
                compra int,
                constraint fk_usuarioavaliacao foreign key (usuario)
                    references usuario(id_usuario),
                constraint fk_compraavaliacao foreign key (compra)
                    references compra(id_compra)
            )"""]
        
        for i in sql:
            self.executar(i, [])

    
    # inserções nas tabelas
    def cadastrar_usuario(self, nome, email, senha, nasci):
        sql = "INSERT INTO usuario(nome, email, senha, nasci) VALUES (%s, %s, %s, %s);"
        self.executar(sql, (nome, email, senha, nasci))

    def cadastrar_sessao(self, ip, ultimo_acesso, usuario):
        sql = "INSERT INTO sessao(ip, ultimo_acesso, usuario) VALUES(%s, %s, %s);"
        self.executar(sql, (ip, ultimo_acesso, usuario))
    
    def cadastrar_cartao(self, numero, nome, cpf, vencimento, cvv, usuario):
        sql = "INSERT INTO cartao(numero, nome, cpf, vencimento, cvv, usuario) VALUES(%s, %s, %s, %s, %s, %s);"
        self.executar(sql, (numero, nome, cpf, vencimento, cvv, usuario))
    
    def cadastrar_endereco(self, estado, cidade, bairro, rua, numero, cep, usuario):
        sql = "INSERT INTO endereco(estado, cidade, bairro, rua, numero, cep, usuario) VALUES(%s, %s, %s, %s, %s, %s, %s);"
        self.executar(sql, (estado, cidade, bairro, rua, numero, cep, usuario))
    
    def cadastrar_produto(self, nome, descricao, ficha_tecnica, valor, estoque, vendedor):
        sql = "INSERT INTO produto(nome, descricao, ficha_tecnica, valor, estoque, vendedor) VALUES(%s, %s, %s, %s, %s, %s);"
        self.executar(sql, (nome, descricao, ficha_tecnica, valor, estoque, vendedor))

    def cadastrar_imagem(self, diretorio, id_produto):
        sql = "INSERT INTO imagem(diretorio, produto) VALUES(%s, %s);"
        self.executar(sql, (diretorio, id_produto))

    def cadastrar_compra(self, quantidade, total, usuario, cartao, endereco, produto):
        sql = "INSERT INTO compra(quantidade, total, usuario, cartao, endereco, produto) VALUES(%s, %s, %s, %s, %s, %s);"
        self.executar(sql, (quantidade, total, usuario, cartao, endereco, produto))

    def cadastrar_avaliacao(self, nota, descricao, usuario, compra):
        sql = "INSERT INTO compra(nota, descricao, usuario, compra) VALUES(%s, %s, %s, %s);"
        self.executar(sql, (nota, descricao, usuario, compra))


    # consultar
    def consultar_usuario(self, email):
        sql = "SELECT * FROM usuario WHERE email=%s"
        return self.consultar(sql, (email,))

    def consultar_sessao(self, ip, usuario):
        sql = "SELECT * FROM sessao WHERE ip=%s AND usuario=%s"
        return self.consultar(sql, (ip, usuario))

    def consultar_cartao(self, id_usuario):
        sql = "SELECT * FROM cartao WHERE usuario=%s"
        return self.consultar(sql, (id_usuario,))

    def consultar_endereco(self, id_usuario):
        sql = "SELECT * FROM endereco WHERE usuario=%s"
        return self.consultar(sql, (id_usuario,))

    def consultar_produto(self, id_usuario):
        sql = "SELECT * FROM produto WHERE vendedor=%s"
        return self.consultar(sql, (id_usuario,))
        
    def produto_especifico(self, id_produto):
        sql = "SELECT * FROM produto WHERE id_produto=%s"
        return self.consultar(sql, (id_produto,))
        
    def consultar_todos_produtos(self):
        sql = "SELECT * FROM produto"
        return self.consultar(sql, ())

    def consultar_imagem(self, id_usuario):
        sql = "SELECT diretorio FROM imagem WHERE produto=%s"
        return self.consultar(sql, (id_usuario,))

    def consultar_compras(self, id_usuario):
        sql = "SELECT * FROM compra WHERE usuario=%s"
        return self.consultar(sql, (id_usuario,))

    def consultar_vendas(self, id_usuario):
        sql = "SELECT * FROM compra JOIN produto ON compra.produto=produto.id_produto WHERE produto.vendedor=%s"
        return self.consultar(sql, (id_usuario,))

    def consultar_avaliacao(self, id_compra):
        sql = "SELECT * FROM avaliacao WHERE compra=%s"
        return self.consultar(sql, (id_compra,))
    
    
    # atualizar
    def atualizar_sessao(self, id_sessao, ultimo_acesso):
        sql = "UPDATE sessao SET ultimo_acesso=%s WHERE id_sessao=%s;"
        self.executar(sql, (ultimo_acesso, id_sessao))
    
    def atualizar_cartao(self, id_cartao, numero, nome, vencimento, cvv, usuario):
        sql = "UPDATE cartao SET numero=%s, nome=%s, vencimento=%s, cvv=%s, usuario=%s WHERE id_cartao=%s;"
        self.executar(sql, (numero, nome, vencimento, cvv, usuario, id_cartao))

    def atualizar_endereco(self, id_endereco, estado, cidade, bairro, rua, numero, cep, usuario):
        sql = "UPDATE endereco SET estado=%s, cidade=%s, bairro=%s, rua=%s, numero=%s, cep=%s, usuario=%s WHERE id_endereco=%s;"
        self.executar(sql, (estado, cidade, bairro, rua, numero, cep, usuario, id_endereco))

    def atualizar_produto(self, id_produto, nome, descricao, ficha_tecnica, valor, estoque, vendedor):
        sql = "UPDATE produto SET nome=%s, descricao=%s, ficha_tecnica=%s, valor=%s, estoque=%s, vendedor=%s WHERE id_produto=%s;"
        self.executar(sql, (nome, descricao, ficha_tecnica, valor, estoque, vendedor, id_produto))

    
    # remoções
    def remover_sessao(self, ip, usuario):
        sql = "DELETE FROM sessao WHERE ip=%s AND usuario=%s;"
        self.executar(sql, (ip, usuario,))

    def remover_cartao(self, id_cartao):
        sql = "DELETE FROM cartao WHERE id_cartao=%s;"
        self.executar(sql, (id_cartao,))

    def remover_endereco(self, id_endereco):
        sql = "DELETE FROM endereco WHERE id_endereco=%s;"
        self.executar(sql, (id_endereco,))

    def remover_produto(self, id_produto):
        sql = "DELETE FROM produto WHERE id_produto=%s;"
        self.executar(sql, (id_produto,))
