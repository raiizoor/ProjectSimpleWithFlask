

class Usuario:
    def __init__(self, nome, usuario, senha, id=None):
        self.id = id
        self.nome = nome
        self.usuario = usuario
        self.senha = senha
    
    @property 
    def is_authenticated(self):
        return True 
    
    @property
    def is_active(self):
        return True

    @property 
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
        
    def __repr__(self):
        return "<User %r>" % self.username

class Jogo:
    def __init__(self, nome, categoria, console, id=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.console = console