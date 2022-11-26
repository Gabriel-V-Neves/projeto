from util.interface import Interface
back = Interface()
from flask import Flask, render_template, request, session, redirect
app = Flask(__name__)
app.secret_key = 'super secret key'


@app.route('/', methods=['GET', 'POST'])
def index():
	if session.get('alerta') and session['alerta'] != "":
		alerta = session['alerta']
		session['alerta'] = ""
		return render_template("index.html", alerta=alerta)
	return render_template("index.html", alerta="")

@app.route('/login', methods=['GET', 'POST'])
def login():
	email = request.form['email']
	senha = request.form['senha']
	num_ip = request.environ['REMOTE_ADDR']
	usuario = back.login(email, senha, num_ip)
	if usuario:
		session['id_usuario'] = usuario
		return redirect('/home')
	return redirect('/')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
	nome = request.form['_nome']
	nasci = request.form['_nasci']
	email = request.form['_email']
	senha = request.form['_senha']
	valido, cadastro = back.cadastrar_usuario(nome, nasci, email, senha)
	if valido:
		num_ip = request.environ['REMOTE_ADDR']
		back.criar_sessao(num_ip, cadastro[0])
		session['id_usuario'] = cadastro[0]
		return redirect('/home')
	session['alerta'] = cadastro
	print(session['alerta'])
	return redirect('/')

@app.route('/home')
def home():
	id_usuario = session['id_usuario']
	produtos = back.consultar_todos_produtos(id_usuario)
	return render_template("home.html", produtos=produtos)

@app.route('/pesquisa', methods=['GET', 'POST'])
def pesquisa():
	pesquisa = request.form['pesquisa']
	id_usuario = session['id_usuario']
	produtos = back.pesquisa_produtos(pesquisa, id_usuario)
	return render_template("home.html", produtos=produtos)

@app.route('/produto', methods=['GET', 'POST'])
def produto():
	produto_selecionado = request.form['produto_selecionado']
	produto = back.produto_especifico(produto_selecionado)
	return render_template("produto.html", produto=produto)

    
@app.route('/compra', methods=['GET', 'POST'])
def compra():
	if session.get('ultimo_produto_observado') and session['ultimo_produto_observado']!="":
		produto = session['ultimo_produto_observado']
	else:
		produto = request.form['compra_produto']
		session['ultimo_produto_observado'] = produto
	id_usuario = session['id_usuario']
	dados_compra = back.dados_compra(produto, id_usuario)
	return render_template("compra.html", dados_compra=dados_compra)

@app.route('/cadastro_compra', methods=['GET', 'POST'])
def cadastro_compra():
	session['ultimo_produto_observado'] = ""
	id_usuario = session['id_usuario']
	id_produto = request.form['produto']
	quantidade = request.form['quantidade']
	cartao = request.form['cartao']
	endereco = request.form['endereco']
	back.cadastro_compra(id_usuario, id_produto, quantidade, cartao, endereco)
	return redirect('/minhas_compras')

@app.route('/meus_dados')
def meus_dados():
	id_usuario = session['id_usuario']
	enderecos = back.consultar_endereco(id_usuario)
	cartoes = back.consultar_cartao(id_usuario)
	if session.get('ultimo_produto_observado'):
		return render_template("meus_dados.html", enderecos=enderecos, cartoes=cartoes, ultimo_produto_observado=session['ultimo_produto_observado'])	
	return render_template("meus_dados.html", enderecos=enderecos, cartoes=cartoes, ultimo_produto_observado="")

@app.route('/cadastro_endereco', methods=['GET', 'POST'])
def cadastro_endereco():
	cep = request.form['cep']
	estado = request.form['estado']
	cidade = request.form['cidade']
	bairro = request.form['bairro']
	rua = request.form['rua']
	numero = request.form['numero']
	complemento = request.form['complemento']
	back.cadastrar_endereco(cep, estado, cidade, bairro, rua, numero, complemento, session['id_usuario'])
	return redirect('meus_dados')

@app.route('/cadastro_cartao', methods=['GET', 'POST'])
def cadastro_cartao():
	nome = request.form['nome']
	cpf = request.form['cpf']
	numero = request.form['numero']
	vencimento = request.form['vencimento']
	cvv = request.form['cvv']
	back.cadastrar_cartao(numero, nome, cpf, vencimento, cvv, session['id_usuario'])
	return redirect('meus_dados')

@app.route('/remover_endereco', methods=['GET', 'POST'])
def remover_endereco():
	endereco = request.form['id_endereco']
	back.remover_endereco(endereco)
	return redirect('meus_dados')

@app.route('/remover_cartao', methods=['GET', 'POST'])
def remover_cartao():
	cartao = request.form['id_cartao']
	back.remover_cartao(cartao)
	return redirect('meus_dados')

@app.route('/minhas_compras')
def minhas_compras():
	id_usuario = session['id_usuario']
	compras = back.consultar_compras(id_usuario)
	return render_template("minhas_compras.html", compras=compras)

@app.route('/produtos_cadastrados')
def produtos_cadastrados():
	id_usuario = session['id_usuario']
	produtos = back.consultar_produtos(id_usuario)
	return render_template("produtos_cadastrados.html", produtos=produtos)
    
@app.route('/vendas_feitas')
def vendas_feitas():
	id_usuario = session['id_usuario']
	vendas = back.consultar_vendas(id_usuario)
	return render_template("vendas_feitas.html", vendas=vendas)

@app.route('/cadastrar_produto')
def cadastrar_produto():
	return render_template("cadastrar_produto.html")

@app.route('/cadastro_produto', methods=['GET', 'POST'])
def cadastro_produto():
	nome = request.form['nome']
	descricao = request.form['descricao']
	ficha_tecnica = request.form['ficha_tecnica']
	valor = request.form['valor']
	estoque = request.form['estoque']
	imagem = request.files['imagem']
	vendedor = session['id_usuario']
	cadastro = back.cadastrar_produto(nome, descricao, ficha_tecnica, valor, estoque, imagem, vendedor)
	
	if cadastro:
		return redirect('/produtos_cadastrados')

	return redirect('/cadastrar_produto')

@app.route('/editar_produto', methods=['GET', 'POST'])
def editar_produto():
	id_produto = request.form['produto_selecionado']
	formulario = back.formulario_edicao(id_produto)
	return render_template("editar_produto.html", formulario=formulario)

@app.route('/edicao_produto', methods=['GET', 'POST'])
def edicao_produto():
	nome = request.form['nome']
	descricao = request.form['descricao']
	ficha_tecnica = request.form['ficha_tecnica']
	valor = request.form['valor']
	estoque = request.form['estoque']
	if 'imagem' not in request.files or request.files['imagem'].filename == "":
		imagem = ""
	else:
		imagem = request.files['imagem']
	vendedor = session['id_usuario']
	back.editar_produto(nome, descricao, ficha_tecnica, valor, estoque, imagem, vendedor, vendedor)
	
	return redirect('/produtos_cadastrados')

@app.route('/remover_produto', methods=['GET', 'POST'])
def remover_produto():
	id_produto = request.form['produto_selecionado']
	back.remover_produto(id_produto)
	return redirect('/produtos_cadastrados')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)