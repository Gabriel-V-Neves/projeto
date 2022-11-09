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

    def criar_tabelas():
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
            create table if not exists cartao(
                id_cartao int auto_increment primary key,
                numero varchar(16),
                nome varchar(50),
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
            )"""
            ]
        
        for i in sql:
            self.executar(i, [])

    # inserções nas tabelas
    def cadastrar_usuario(nome, email, senha, nasci):
        sql = "INSERT INTO usuario(nome, email, senha, nasci) VALUES(%s, %s, password(%s), %s);"
        self.executar(sql, (nome, email, senha, nasci))

    def cadastrar_cartao(numero, nome, vencimento, cvv, usuario):
        sql = "INSERT INTO cartao(numero, nome, vencimento, cvv, usuario) VALUES(%s, %s, %s, %s, %s);"
        self.executar(sql, (numero, nome, vencimento, cvv, usuario))
    
    def cadastrar_endereco(estado, cidade, bairro, rua, numero, cep, usuario):
        sql = "INSERT INTO endereco(estado, cidade, bairro, rua, numero, cep, usuario) VALUES(%s, %s, %s, %s, %s, %s, %s);"
        self.executar(sql, (estado, cidade, bairro, rua, numero, cep, usuario))
    
    def cadastrar_produto(nome, descricao, ficha_tecnica, valor, estoque, vendedor):
        sql = "INSERT INTO produto(nome, descricao, ficha_tecnica, valor, estoque, vendedor) VALUES(%s, %s, %s, %s, %s, %s);"
        self.executar(sql, (nome, descricao, ficha_tecnica, valor, estoque, vendedor))

    def cadastrar_compra(quantidade, total, usuario, cartao, endereco, produto):
        sql = "INSERT INTO compra(quantidade, total, usuario, cartao, endereco, produto) VALUES(%s, %s, %s, %s, %s, %s);"
        self.executar(sql, (quantidade, total, usuario, cartao, endereco, produto)

    def cadastrar_avaliacao(nota, descricao, usuario, compra):
        sql = "INSERT INTO compra(nota, descricao, usuario, compra) VALUES(%s, %s, %s, %s);"
        self.executar(sql, (nota, descricao, usuario, compra)


'''cnx = mysql.connector.connect(user='root',
                             password='99227512Biel*',
                             host='localhost',
                             database='projeto')
cursor = cnx.cursor()'''




'''# 2
var_ind = input("Qual o nome do índice? ")
var_resp = input("Quem é o responsável pelo cálculo? ")


sql = """
INSERT INTO tb_ind(nme_ind, nme_resp_calc_ind)
    VALUES(%s, %s);
"""
cursor.execute(sql, (var_ind, var_resp))
cnx.commit()
'''
