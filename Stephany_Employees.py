import google.generativeai as genai
import textwrap
from Database import Database
import json
import os

class Stephany2:

    def __init__(self, api_key, db_config, history_file='chat_employees_history.json'):
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

        # Formateamos el historial para que esté en el formato correcto
        formatted_history = self.format_history()

        # Iniciamos el chat
        self.chat = self.model.start_chat(history=formatted_history, enable_automatic_function_calling=True)

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as file:
                self.history = json.load(file)
        else:
            self.history = []

    def save_history(self):
        with open(self.history_file, 'w') as file:
            json.dump(self.history, file, indent=4)

    def format_history(self):
        formatted_history = []
        for entry in self.history:
            formatted_history.append({
                'parts': [{'text': entry['user']}],
                'role': 'user'
            })
            formatted_history.append({
                'parts': [{'text': entry['gemini']}],
                'role': 'model'
            })
        return formatted_history

    # Esta función se usa para dejar el formato de la respuesta en un formato legible
    def to_markdown(self, text):
        text = text.replace('•', '  *')
        return textwrap.indent(text, '> ', predicate=lambda _: True)

    # Enviamos un mensaje y recibimos la respuesta
    def send_message(self, message):
        if self.first:
            # Extraemos la información relevante de la base de datos
            context = self.get_context()

            context_luthymakeup = ("Hola, voy a usarte como parte de un chatbot para mi negocio de maquillaje llamado LuthyMakeup")
            
            # Decirle que no se salga del contexto
            context_luthymakeup = (
                "Hola, voy a usarte como parte de un chatbot para mi negocio de maquillaje llamado LuthyMakeup "
                "(con sede en Barranquilla, Colombia). En esta sección, solo responderás preguntas y solicitudes relacionadas con los empleados "
                "de la empresa y la información operativa que se encuentra en las tablas que te enviaré. Este chat está enfocado en la parte "
                "operativa de la empresa y sus funcionalidades. "

                "Importante: "
                "1. Si la pregunta que te hago es ambigua, di: 'Dame más información para darte una respuesta concreta.' "
                "2. Si la pregunta que te hago no tiene nada que ver con la empresa o el enfoque del chatbot, por favor di: 'No puedo responder a esa pregunta.' "

                "Solo responde preguntas relacionadas con la empresa y la información de las tablas que te proporcionaré."
            )

            # Incluimos el contexto en el mensaje
            full_message = f"{context_luthymakeup}\n\n{context}\n\n{message}"
            self.first = False
        else:
            full_message = "\n".join([f"User: {entry['user']}\nGemini: {entry['gemini']}" for entry in self.history])
            full_message += f"\nUser: {message}"

        try:
            # Enviamos el mensaje a Gemini
            response = self.chat.send_message(full_message)
            formatted_response = self.to_markdown(response.text)

            # Guardamos el mensaje y la respuesta en el historial
            self.history.append({'user': message, 'gemini': formatted_response})
            self.save_history()

            return formatted_response
        except genai.types.generation_types.StopCandidateException as e:
            print("La respuesta fue detenida por motivos de seguridad:", e)
            return "Lo siento, no puedo proporcionar una respuesta a esa pregunta, intenta preguntar de otra manera."

    # Función para obtener contexto de la base de datos
    def get_context(self):
        products = self.get_products()
        clients = self.get_clients()
        orders = self.get_orders()
        employees = self.get_employees()

        context = "Productos:\n" + self.format_table(products)
        context += "\n\nClientes:\n" + self.format_table(clients)
        context += "\n\nÓrdenes:\n" + self.format_table(orders)
        context += "\n\nEmpleados:\n" + self.format_table(employees)

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
        query = "SELECT * FROM data.Orders_2"
        return self.db.execute_query(query)

    # Función para obtener empleados
    def get_employees(self):
        query = "SELECT * FROM data.Employees_3"
        return self.db.execute_query(query)

    # Función para formatear las tablas en texto plano
    def format_table(self, data):
        if not data:
            return "No se encontraron resultados."

        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            headers = data[0].keys()
            table = "| " + " | ".join(headers) + " |\n"
            table += "|---" * len(headers) + "|\n"
            for row in data:
                table += "| " + " | ".join(map(str, row.values())) + " |\n"
        else:
            headers = [f"Columna {i+1}" for i in range(len(data[0]))]
            table = "| " + " | ".join(headers) + " |\n"
            table += "|---" * len(headers) + "|\n"
            for row in data:
                table += "| " + " | ".join(map(str, row)) + " |\n"

        return table