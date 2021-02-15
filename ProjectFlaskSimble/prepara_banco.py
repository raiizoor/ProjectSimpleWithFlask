import MySQLdb
print('Conectando...')
conn = MySQLdb.connect(user='root', passwd='admin', host='127.0.0.1', port=3306)

# Descomente se quiser desfazer o banco...
# Primeira vez que for criar o Banco de dados...
# é necessário alterar a linha 9 para CREATE DATABASE executar.
# Depois alterar novamente para DROP DATABAS, excutar e o Banco sera criado.
#conn.cursor().execute("DROP DATABASE `jogoteca`;")
#conn.commit()

criar_tabelas = '''SET NAMES latin1;
    CREATE DATABASE `jogoteca` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
    USE `jogoteca`;
    CREATE TABLE `jogo` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) COLLATE utf8_bin NOT NULL,
      `categoria` varchar(40) COLLATE utf8_bin NOT NULL,
      `console` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE `usuario` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) COLLATE utf8_bin NOT NULL,
      `usuario` varchar(20) COLLATE utf8_bin NOT NULL,
      `senha` varchar(15) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

conn.cursor().execute(criar_tabelas)

# inserindo usuarios
cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO jogoteca.usuario (nome, usuario, senha) VALUES (%s, %s, %s)',
      [
            ('Luan Marques', 'luan', 'flask'),
            ('Nico', 'nico', '7a1'),
            ('Danilo', 'danilo', 'vegas')
      ])

cursor.execute('select * from jogoteca.usuario')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
cursor.executemany(
      'INSERT INTO jogoteca.jogo (nome, categoria, console) VALUES (%s, %s, %s)',
      [
      ])

cursor.execute('select * from jogoteca.jogo')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()