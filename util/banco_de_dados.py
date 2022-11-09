import mysql.connector

cnx = mysql.connector.connect(user='root',
                             password='99227512Biel*',
                             host='localhost',
                             database='projeto')
cursor = cnx.cursor()

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
    cursor.execute(i, [])
    cnx.commit()


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