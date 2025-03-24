from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin  # Importar UserMixin para Flask-Login
import datetime

db = SQLAlchemy()

# Modelo de usuario para autenticación
class User(UserMixin, db.Model):  # Heredar de UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='empleado')  # 'admin' o 'empleado'

    # Flask-Login ya proporciona los métodos necesarios a través de UserMixin
    # No es necesario definir is_active, is_authenticated, is_anonymous o get_id manualmente

# Modelo de pedidos (ya existente en tu proyecto)
class Pedidos(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.String(100))
    telefono = db.Column(db.String(100))
    fecha_compra = db.Column(db.DateTime, default=datetime.datetime.now)
    total_pedido = db.Column(db.Float)

# Modelo de profesor (opcional)
class Profesor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    materia = db.Column(db.String(100), nullable=False)