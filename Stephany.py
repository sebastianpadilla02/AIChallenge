import google.generativeai as genai
import textwrap
from Database import Database

class Stephany:

    def __init__(self, api_key, db_config):
        self.api_key = api_key
        self.history = []
        self.db = Database(db_config)
        self.configure()

    def initialize(self):
        # Configuramos nuestra instancia del modelo con nuestra API key
        genai.configure(api_key=self.api_key)
        # Inicializamos el modelo
        self.model = genai.GenerativeModel('gemini-pro', )
        # Iniciamos el chat
        self.chat = self.model.start_chat(self.history)


    def get_historiy(self):
        return self.chat.history

    # Esta función se usa para dejar el formato de la respuesta en un formato legible
    def to_markdown(self, text):
        text = text.replace('•', '  *')
        return textwrap.indent(text, '> ', predicate=lambda _: True)

    # Enviamos un mensaje y recibimos la respuesta
    def send_message(self, message):
        if "productos" in message.lower():
            products = self.get_products()
            return self.format_table(products)
        elif "clientes" in message.lower():
            clients = self.get_clients()
            return self.format_table(clients)
        elif "órdenes" in message.lower():
            orders = self.get_orders()
            return self.format_table(orders)
        else:
            response = self.model.chat(message)
            formatted_response = self.to_markdown(response.text)
            return formatted_response

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

    # Función para formatear las tablas en Markdown
    def format_table(self, data):
        if not data:
            return "No se encontraron resultados."
        
        headers = [i[0] for i in self.db.cursor.description]
        table = "| " + " | ".join(headers) + " |\n"
        table += "|---" * len(headers) + "|\n"
        for row in data:
            table += "| " + " | ".join(map(str, row)) + " |\n"
        
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

    stephany = Stephany(api_key, db_config)
    message = "Que productos valen mas?"
    response = Stephany.send_message(message)
    print(response)
