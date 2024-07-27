import google.generativeai as genai
import textwrap

# Esta función se usa para dejar el formato de la respuesta en un formato legible
def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Configuramos nuestra instancia del modelo con nuestra API key
GOOGLE_API_KEY = 'AIzaSyDR-yzVIRiFoQqWsdT3tNX2BcR_T4TcAQQ'
genai.configure(api_key=GOOGLE_API_KEY)

# Inicializamos el modelo
model = genai.GenerativeModel('gemini-pro')

# Iniciamos el chat
chat = model.start_chat(history=[])

# Enviamos un mensaje y recibimos la respuesta
response = chat.send_message("Vivo en Chile. Describe brevemente mi país")

# Formateamos la respuesta
formatted_response = to_markdown(response.text)

# Imprimimos la respuesta formateada
print(formatted_response)
