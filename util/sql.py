import mysql.connector


class Database():
    def __init__(self, user, password, host, database):
        self.cnx = mysql.connector.connect(user=user,
                                           password=password,
                                           host=host,
                                           database=database)

    def executar(self, comando, parametros):
        cs = self.cnx.cursor()
        cs.execute(comando, parametros)
        self.cnx.commit()
        cs.close()

    def consultar(self, comando, parametros):
        cs = self.cnx.cursor()
        cs.execute(comando, parametros)
        result = []
        for i in cs:
            result.append(i)
        return result

    def __del__(self):
        self.cnx.close()


db = Database('root', '99227512Biel*', 'localhost', 'projeto')

sql = "drop database projeto;"
db.executar(sql, [])
sql = "create database projeto"
db.executar(sql, [])
