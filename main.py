from util.interface import Interface
back = Interface()
from flask import Flask, render_template, request, session, redirect
app = Flask(__name__)
app.secret_key = 'super secret key'

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/login')
def login():
	return render_template("login.html")

@app.route('/produto')
def produto():
	return render_template("produto.html")
    
@app.route('/compra')
def compra():
	return render_template("compra.html")

@app.route('/meus_dados')
def meus_dados():
	return render_template("meus_dados.html")

@app.route('/minhas_compras')
def minhas_compras():
	return render_template("minhas_compras.html")

@app.route('/produtos_cadastrados')
def produtos_cadastrados():
	return render_template("produtos_cadastrados.html")
    
@app.route('/vendas_feitas')
def vendas_feitas():
	return render_template("vendas_feitas.html")

@app.route('/cadastrar_produto')
def cadastrar_produto():
	return render_template("cadastrar_produto.html")