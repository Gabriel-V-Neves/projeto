from util.interface import Interface
back = Interface()
from flask import Flask, render_template, request, session, redirect
app = Flask(__name__)
app.secret_key = 'super secret key'


@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template("index.html")

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
	cadastro = back.cadastrar_usuario(nome, nasci, email, senha)
	if cadastro:
		num_ip = request.environ['REMOTE_ADDR']
		back.criar_sessao(num_ip, cadastro[0])
		return redirect('/home')
	return redirect('/')

@app.route('/home')
def menu():
	return render_template("home.html")

@app.route('/produto')
def produto():
	return render_template("produto.html")
    
@app.route('/compra')
def compra():
	return render_template("compra.html")

@app.route('/meus_dados')
def meus_dados():
	return render_template("meus_dados.html")

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

@app.route('/cadastro_produto', methods=['GET', 'POST'])
def cadastro_produto():
	nome = request.form['nome']
	descricao = request.form['descricao']
	ficha_tecnica = request.form['ficha_tecnica']
	valor = request.form['valor']
	estoque = request.form['estoque']
	#imagem_nome = request.form['imagem']
	imagem = request.files['imagem']
	print(imagem)
	vendedor = session['id_usuario']
	cadastro = back.cadastrar_produto(nome, descricao, ficha_tecnica, valor, estoque, imagem, vendedor)
	
	if cadastro:
		return redirect('/produtos_cadastrados')

	'''
	if imagem and arquivo_permitido(imagem.filename):
		cadastro = back.cadastrar_produto() #terminar
		if cadastro:
			nome_imagem = #id_usuario-id_produto-datetime
			imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_imagem))
			#cadastrar url da imagem
			return redirect('/produtos_cadastrados')'''
	return redirect('/cadastrar_produto')

