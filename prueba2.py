import google.generativeai as genai
import textwrap
import logging
from Database import Database

class Gemini:

    def __init__(self, api_key, db_config):
        self.api_key = api_key
        self.history = []
        self.db = Database(db_config)
        self.configure()

    def configure(self):
        # Configuramos nuestra instancia del modelo con nuestra API key
        genai.configure(api_key=self.api_key)

        # Inicializamos el modelo
        self.model = genai.GenerativeModel('gemini-pro')

        self.chat = self.model.start_chat(history = self.history,enable_automatic_function_calling = True)

    # Esta función se usa para dejar el formato de la respuesta en un formato legible
    def to_markdown(self, text):
        text = text.replace('•', '  *')
        return textwrap.indent(text, '> ', predicate=lambda _: True)

    # Enviamos un mensaje y recibimos la respuesta
    def send_message(self, message):
        # Extraemos la información relevante de la base de datos
        context = self.get_context()
        
        # Incluimos el contexto en el mensaje
        full_message = f"{context}\n\n{message}"
        
        # Enviamos el mensaje a Gemini
        response = self.chat.send_message(full_message)
        formatted_response = self.to_markdown(response.text)
        return formatted_response

    # Función para obtener contexto de la base de datos
    def get_context(self):
        products = self.get_products()
        clients = self.get_clients()
        orders = self.get_orders()

        context = "Productos:\n" + self.format_table(products)
        context += "\n\nClientes:\n" + self.format_table(clients)
        context += "\n\nÓrdenes:\n" + self.format_table(orders)
        
        return context

    # Función para obtener productos
    def get_products(self):
        query = "SELECT * FROM data.Products"
        return self.db.execute_query(query)

    # Función para obtener clientes
    def get_clients(self):
        query = "SELECT * FROM data.Clients"
        return self.db.execute_query(query)

    # Función para obtener órdenes
    def get_orders(self):
        query = "SELECT * FROM data.Orders"
        return self.db.execute_query(query)

    # Función para formatear las tablas en texto plano
    def format_table(self, data):
        if not data:
            return "No se encontraron resultados."
        
        headers = data[0].keys()
        table = "| " + " | ".join(headers) + " |\n"
        table += "|---" * len(headers) + "|\n"
        for row in data:
            table += "| " + " | ".join(map(str, row.values())) + " |\n"
        
        return table

# Uso de la clase
if __name__ == "__main__":
    api_key = 'AIzaSyDR-yzVIRiFoQqWsdT3tNX2BcR_T4TcAQQ'
    
    db_config = {
        'user': 'avnadmin',
        'password': 'AVNS_fOnqMRAe1yWi236icem',
        'host': 'mysql-luthymakeup-luthymakeup.i.aivencloud.com',
        'database': 'defaultdb',
        'port': '13214'
    }

    gemini = Gemini(api_key, db_config)
    message = "Dame un codigo para sumar dos numeros en python"
    response = gemini.send_message(message)
    print(response)
