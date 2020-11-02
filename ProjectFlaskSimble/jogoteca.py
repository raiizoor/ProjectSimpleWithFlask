from flask import Flask, render_template, request, redirect, session, flash, url_for
from models import Jogo, Usuario
from DAO import JogoDao, UsuarioDao
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'alura'

app.config['MYSQL_HOST'] = "127.0.0.1"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "admin"
app.config['MYSQL_DB'] = "jogoteca"
app.config['MYSQL_PORT'] = 3306
db = MySQL(app)

jogo_dao = JogoDao(db)

usuario_dao = UsuarioDao(db)

@app.route('/')
def index():
    lista = jogo_dao.listar()
    return render_template('lista.html', titulo='Jogos', jogos=lista) 

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('novo')))
    return render_template('AdicionarNovoJogo.html', titulo = 'Adicionar Novo Jogo')

@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogos = Jogo(nome, categoria, console)
    jogo_dao.salvar(jogos)

    arquivo = request.files['arquivo']
    arquivo.save(f'uploads/{arquivo.filename}')
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('editar', id=id)))
    jogo = jogo_dao.busca_por_id(id)
    return render_template('editar.html', titulo = 'Editar o Jogo.', jogo=jogo)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogos = Jogo(nome, categoria, console, id=request.form['id'])
    jogo_dao.salvar(jogos)
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    jogo_dao.deletar(id)
    flash('O jogo foi deletado com sucesso.')
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session ['usuario_logado'] = usuario.id
            flash(usuario.nome + ' Logado com sucesso!')
            proxima_pagina =  request.form['proxima']
            return redirect(proxima_pagina)
        else: 
            flash('Usuario ou senha errados, porvafor tente novamente.')
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session ['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

app.run(debug = True)
