from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
import time

from models import Jogo, Usuario
from DAO import JogoDao, UsuarioDao

from helpers import recupera_imagem, deleta_arquivo
from jogoteca import db, app

jogo_dao = JogoDao(db)

usuario_dao = UsuarioDao(db)

@app.route('/')
def index():
    lista = jogo_dao.listar()
    return render_template('ListGames.html', titulo='Jogos', jogos=lista) 

@app.route('/listuser')
def listuser():
    lista = usuario_dao.listar()
    return render_template('ListUsers.html', titulo='Adicionar Novo Usuario', usuarios=lista) 

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('novo')))
    return render_template('AddNewGame.html', titulo = 'Adicionar Novo Jogo')

@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogos = Jogo(nome, categoria, console)
    jogo = jogo_dao.salvar(jogos)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
    return redirect(url_for('index'))

@app.route('/createuser', methods=['POST', ])
def createuser():
    nome = request.form['nome']
    usuario = request.form['usuario']
    senha = request.form['senha']
    usuarios = Usuario(nome, usuario, senha)
    usuario = usuario_dao.salvar(usuarios)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{usuario.id}-{timestamp}.jpg')
    return redirect(url_for('listuser'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('editar', id=id)))
    jogo = jogo_dao.busca_por_id(id)
    nome_imagem = recupera_imagem(id)
    return render_template('EditListGames.html', titulo = 'Editar o Jogo.', jogo = jogo,
                            capa_jogo = nome_imagem)

@app.route('/edituser/<int:id>')
def edituser(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('editar', id=id)))
    usuario = usuario_dao.buscar_por_id(id)
    nome_imagem = recupera_imagem(id)
    return render_template('EditListUser.html', titulo = 'Editar o Usuario.', usuario = usuario,
                            foto_usuario = nome_imagem)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console, id=request.form['id'])
    jogo_dao.salvar(jogo)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(jogo.id)
    arquivo.save( f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
    return redirect(url_for('index'))

@app.route('/atualizaruser', methods=['POST',])
def atualizaruser():
    nome = request.form['nome']
    usuario = request.form['usuario']
    senha = request.form['senha']
    usuario = Usuario(nome, usuario, senha, id=request.form['id'])
    usuario_dao.salvar(usuario)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(usuario.id)
    arquivo.save( f'{upload_path}/capa{usuario.id}-{timestamp}.jpg')
    return redirect(url_for('listuser'))

@app.route('/deletar/<int:id>')
def deletar(id):
    deleta_arquivo(id)
    jogo_dao.deletar(id)
    flash('O jogo foi deletado com sucesso.')
    return redirect(url_for('index'))

@app.route('/deleteuser/<int:id>')
def deleteuser(id):
    deleta_arquivo(id)
    usuario_dao.deletar(id)
    flash('O Usuario foi deletado com sucesso.')
    return redirect(url_for('listuser'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.buscar_por_usuario(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session ['usuario_logado'] = usuario.id
            flash(usuario.nome + ' Logado com sucesso!')
            proxima_pagina =  request.form['proxima']
            return redirect(proxima_pagina)
        else: 
            flash('Usuario ou senha errados, porfavor tente novamente.')
            return redirect(url_for('login'))

@app.route('/signup')
def signup():
    return render_template('AddNewUser.html')

@app.route('/logout')
def logout():
    session ['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))