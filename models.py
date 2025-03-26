from extensions import db
from flask_login import UserMixin
import datetime

class Pedidos(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.String(100))
    telefono = db.Column(db.String(100))
    fecha_compra = db.Column(db.DateTime, default=datetime.datetime.now)
    total_pedido = db.Column(db.Float)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'proveedor' o 'cliente'
    eliminado = db.Column(db.Boolean, default=False)
    # Relación con Proveedor
    proveedor = db.relationship('Proveedor', back_populates='usuario', uselist=False, cascade='all, delete-orphan')

class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    calle = db.Column(db.String(100))
    telefono = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    eliminado = db.Column(db.Boolean, default=False)
    # Relación bidireccional
    usuario = db.relationship('User', back_populates='proveedor')

def load_user(user_id):
    return User.query.get(int(user_id))