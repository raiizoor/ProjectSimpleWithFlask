from models import Jogo, Usuario

SQL_DELETA_JOGO = 'delete from jogo where id = %s'
SQL_DELETA_USUARIO = 'delete from usuario where id = %s'
SQL_JOGO_POR_ID = 'SELECT id, nome, categoria, console from jogo where id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, nome, usuario, senha from usuario where id = %s'
SQL_USUARIO_POR_USUARIO = 'SELECT id, nome, usuario, senha from usuario where usuario = %s'
SQL_USUARIO_POR_SENHA = 'SELECT id, nome, usuario, senha from usuario where senha = %s'
SQL_ATUALIZA_JOGO = 'UPDATE jogo SET nome=%s, categoria=%s, console=%s where id = %s'
SQL_ATUALIZA_USUARIO = 'UPDATE usuario SET nome=%s, usuario=%s, senha=%s where id = %s'
SQL_BUSCA_JOGOS = 'SELECT id, nome, categoria, console from jogo'
SQL_BUSCA_USUARIOS = 'SELECT id, nome, usuario, senha from usuario'
SQL_CRIA_JOGO = 'INSERT into jogo (nome, categoria, console) values (%s, %s, %s)'
SQL_CRIA_USUARIO = 'INSERT into usuario(nome, usuario, senha) values (%s, %s, %s)'

class JogoDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, jogo):
        cursor = self.__db.connection.cursor()

        if (jogo.id):
            cursor.execute(SQL_ATUALIZA_JOGO, (jogo.nome, jogo.categoria, jogo.console, jogo.id))
        else:
            cursor.execute(SQL_CRIA_JOGO, (jogo.nome, jogo.categoria, jogo.console))
            jogo.id = cursor.lastrowid
        self.__db.connection.commit()
        return jogo

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_JOGOS)
        jogos = traduz_jogos(cursor.fetchall())
        return jogos

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_JOGO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_JOGO, (id, ))
        self.__db.connection.commit()


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, usuario):
        cursor = self.__db.connection.cursor()

        if (usuario.id):
            cursor.execute(SQL_ATUALIZA_USUARIO, (usuario.nome, usuario.usuario, usuario.senha, usuario.id))
        else:
            cursor.execute(SQL_CRIA_USUARIO, (usuario.nome, usuario.usuario, usuario.senha))
            usuario.id = cursor.lastrowid
        self.__db.connection.commit()
        return usuario
    
    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_USUARIOS)
        usuarios = traduz_usuario(cursor.fetchall())
        return usuarios
    
    def buscar_por_usuario(self, usuario):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_USUARIO, (usuario,))
        tupla = cursor.fetchone()
        return Usuario(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def buscar_por_senha(self, senha):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_SENHA, (senha,))
        tupla = cursor.fetchone()
        return Usuario(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Usuario(tupla[1], tupla[2], tupla[3], id=tupla[0])
        
    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_USUARIO, (id, ))
        self.__db.connection.commit()

   
def traduz_jogos(jogos):
    def cria_jogo_com_tupla(tupla):
        return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(cria_jogo_com_tupla, jogos))


def traduz_usuario(usuarios):
    def cria_usuario_com_tupla(tupla):
        return Usuario(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(cria_usuario_com_tupla, usuarios))

