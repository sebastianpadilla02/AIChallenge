from .ConexionBD import ConexionBD
from .AI import AI
from flask import Flask, render_template, request, jsonify

class App:

    def __init__ (self):
        self.base_datos = ConexionBD()
        self.AI = AI()
    
    def registrarUsuario (self, nombre, email, direccion, telefono, contra):
        pass
    
    def realizarOrdenCompra (self, email, producto):
        pass
    
    def obtenerDatosUsuario (self):
        pass
    
    def actualizarCatalogo (self):
        pass
    
    def obtenerRespuesta (self, consulta):
        return self.AI.obtenerRespuesta(consulta)


app = Flask(__name__)
aplicacion = App()

@app.route("/")
def index():
    print("[MENSAJE]: BackEnd inicializado")    
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    return aplicacion.obtenerRespuesta(input)

print("[MENSAJE]: BackEnd inicializado")    
