from flask import render_template, request, redirect, session, flash, url_for
import time

from models import Usuario
from DAO import UsuarioDao

from helpers import recupera_imagem, deleta_arquivo, imagem
from jogoteca import app, db

usuario_dao = UsuarioDao(db)


@app.route('/listuser')
def listuser():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('listuser')))
    lista = usuario_dao.listar()
    return render_template('ListUsers.html', titulo='Usuario', usuarios=lista) 

@app.route('/signup')
def signup():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('signup')))
    return render_template('AddNewUser.html', titulo = 'Adicionar Novo Usuario')

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

@app.route('/edituser/<int:id>')
def edituser(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('editar', id=id)))
    usuario = usuario_dao.buscar_por_id(id)
    nome_imagem = recupera_imagem(id)
    return render_template('EditListUser.html', titulo = 'Editar o Usuario.', usuario = usuario,
                                                foto_usuario = nome_imagem)

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


@app.route('/deleteuser/<int:id>')
def deleteuser(id):
    deleta_arquivo(id)
    usuario_dao.deletar(id)
    flash('O Usuario foi deletado com sucesso.')
    return redirect(url_for('listuser'))
