import google.generativeai as genai
import textwrap
from Database import Database
import json
import os

class Stephany:

    def __init__(self, api_key, db_config, history_file='chat_history.json'):
        self.first = True
        self.api_key = api_key
        self.db = Database(db_config)
        self.history_file = history_file
        self.load_history()
        self.configure()

    def configure(self):
        # Configuramos nuestra instancia del modelo con nuestra API key
        genai.configure(api_key=self.api_key)

        # Inicializamos el modelo
        self.model = genai.GenerativeModel('gemini-pro')

        self.chat = self.model.start_chat(history = self.history,enable_automatic_function_calling = True)

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as file:
                self.history = json.load(file)
        else:
            self.history = []

    def save_history(self):
        with open(self.history_file, 'w') as file:
            json.dump(self.history, file, indent=4)

    # Esta función se usa para dejar el formato de la respuesta en un formato legible
    def to_markdown(self, text):
        text = text.replace('•', '  *')
        return textwrap.indent(text, '> ', predicate=lambda _: True)

    # Enviamos un mensaje y recibimos la respuesta
    def send_message(self, message):
        if(self.first):
            # Extraemos la información relevante de la base de datos
            context = self.get_context()
        
            # Incluimos el contexto en el mensaje
            full_message = f"{context}\n\n{message}"
            self.first = False
        else:
            # Extraemos la información relevante de la base de datos
            full_message = "\n".join([f"User: {entry['user']}\nGemini: {entry['gemini']}" for entry in self.history])
            full_message += f"\nUser: {message}"
        
        # Enviamos el mensaje a Gemini
        response = self.chat.send_message(full_message)
        formatted_response = self.to_markdown(response.text)

        # Guardamos el mensaje y la respuesta en el historial
        self.history.append({'user': message, 'gemini': formatted_response})
        self.save_history()
        
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

