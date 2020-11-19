

class Usuario:
    def __init__(self, nome, usuario, senha, id=None):
        self.id = id
        self.nome = nome
        self.usuario = usuario
        self.senha = senha

class Jogo:
    def __init__(self, nome, categoria, console, id=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.console = console