from flask import render_template, request, redirect, session, flash, url_for
from flask_login import login_user
import time

from models import Jogo, Usuario
from DAO import JogoDao

from helpers import recupera_imagem, deleta_arquivo, imagem
from jogoteca import app, db, lm
from form import LoginForm

jogo_dao = JogoDao(db)

from back_end_users import *

@lm.user_loader
def load_user(id):
    return usuario_dao.buscar_por_id(request.form['id'])

@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    lista = jogo_dao.listar()
    return render_template('ListGames.html', titulo='Jogos', jogos=lista) 

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
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

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    jogo = jogo_dao.busca_por_id(id)
    nome_imagem = recupera_imagem(id)
    return render_template('EditListGames.html', titulo = 'Editar o Jogo.', jogo = jogo,
                            capa_jogo = nome_imagem)

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

@app.route('/deletar/<int:id>')
def deletar(id):
    deleta_arquivo(id)
    jogo_dao.deletar(id)
    flash('O jogo foi deletado com sucesso.')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = usuario_dao.buscar_por_usuario(request.form['usuario'])
        if usuario and usuario.usuario == form.senha.data:
            login_user(usuario)
            flash("Logado com sucesso.")
            return redirect(url_for("index"))
        else:
            flash("Usuario invalido.")

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session ['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))