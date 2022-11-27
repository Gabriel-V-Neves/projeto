from banco_de_dados import Database

db = Database('root', '12345678', 'localhost', 'projeto')
sql = 'drop database projeto'
db.executar(sql, [])
'''sql = 'create database projeto'
db.executar(sql, [])
sql = 'use projeto'
db.executar(sql, [])
db.criar_tabelas()
'''