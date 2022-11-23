from banco_de_dados import Database

print("Iniciando banco de dados...")
db = Database('root', '12345678', 'localhost', 'projeto')
print("Criando tabelas...")
db.criar_tabelas()
print("Tabelas criadas.")

print("\nConfiguração concluída!")
