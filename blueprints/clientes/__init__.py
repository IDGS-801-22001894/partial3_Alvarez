from flask import Blueprint

clientes_bp = Blueprint('clientes', __name__, template_folder='../templates')

# Importar rutas después de definir el blueprint para evitar dependencia circular
from . import routes