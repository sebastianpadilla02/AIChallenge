import mysql.connector

class Database:
    
    def __init__(self, config):
        self.config = config
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor(dictionary=True)  # Usamos dictionary=True para obtener los resultados como diccionarios
            print("Conexión a la base de datos exitosa")
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None

    def close(self):
        self.cursor.close()
        self.conn.close()
