from flask import Blueprint
from extensions import db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Pedidos
from forms import PedidoForm
import os
import datetime
from sqlalchemy import func

clientes_bp = Blueprint('clientes', __name__, template_folder='../../../templates')

PEDIDOS_TEMP_FILE = 'pedidos.txt'

def calcular_subtotal(tamaño, ingredientes, cantidad):
    precio_tamaño = {'Chica': 40, 'Mediana': 80, 'Grande': 120}.get(tamaño, 0)
    precio_ingredientes = len(ingredientes) * 10
    return (precio_tamaño + precio_ingredientes) * cantidad

def guardar_pedido_temporal(tamaño, ingredientes, cantidad, subtotal):
    with open(PEDIDOS_TEMP_FILE, 'a') as f:
        f.write(f"{tamaño},{','.join(ingredientes)},{cantidad},{subtotal}\n")

def leer_pedidos_temporales():
    pedidos = []
    if os.path.exists(PEDIDOS_TEMP_FILE):
        with open(PEDIDOS_TEMP_FILE, 'r') as f:
            for line in f:
                valores = line.strip().split(',')
                if len(valores) >= 4:  
                    tamaño = valores[0]
                    ingredientes = valores[1:-2]  
                    cantidad = int(valores[-2])
                    subtotal = float(valores[-1])

                    pedidos.append({
                        'tamaño': tamaño,
                        'ingredientes': ingredientes,
                        'cantidad': cantidad,
                        'subtotal': subtotal
                    })
    return pedidos

def limpiar_pedidos_temporales():
    if os.path.exists(PEDIDOS_TEMP_FILE):
        os.remove(PEDIDOS_TEMP_FILE)

@clientes_bp.route("/", methods=['GET', 'POST'])
@login_required
def pedido():
    form = PedidoForm()
    pedidos_temporales = leer_pedidos_temporales()
    total_pedido_temporal = sum(pedido['subtotal'] for pedido in pedidos_temporales)

    nombre_cliente = request.args.get('nombre', '')
    direccion_cliente = request.args.get('direccion', '')
    telefono_cliente = request.args.get('telefono', '')

    fecha = request.form.get('fecha')
    periodo = request.form.get('periodo', 'dia')
    ventas = []
    total_ventas = 0.0 

    if fecha:
        try:
            fecha_dt = datetime.datetime.strptime(fecha, '%Y-%m-%d')
            if periodo == 'dia':
                ventas = Pedidos.query.filter(func.date(Pedidos.fecha_compra) == fecha_dt.date()).all()
                total_ventas = sum(pedido.total_pedido for pedido in ventas)
            else:  
                ventas = Pedidos.query.filter(func.strftime('%Y-%m', Pedidos.fecha_compra) == fecha_dt.strftime('%Y-%m')).all()
                total_ventas = sum(pedido.total_pedido for pedido in ventas)
        except ValueError:
            flash("Formato de fecha incorrecto. Use AAAA-MM-DD.", "danger")

    if form.validate_on_submit():
        tamaño_pizza = form.tamaño_pizza.data
        ingredientes = form.ingredientes.data
        numero_pizzas = form.numero_pizzas.data
        subtotal = calcular_subtotal(tamaño_pizza, ingredientes, numero_pizzas)
        guardar_pedido_temporal(tamaño_pizza, ingredientes, numero_pizzas, subtotal)
        flash(f"Pizza agregada al pedido. Subtotal: ${subtotal:.2f}", "success")
        return redirect(url_for('clientes.pedido', nombre=form.nombre.data, 
                              direccion=form.direccion.data, telefono=form.telefono.data))

    form.nombre.data = nombre_cliente
    form.direccion.data = direccion_cliente
    form.telefono.data = telefono_cliente

    return render_template('index.html', form=form, pedidos=pedidos_temporales,
                         total_pedido=total_pedido_temporal, nombre_cliente=nombre_cliente,
                         direccion_cliente=direccion_cliente, telefono_cliente=telefono_cliente,
                         ventas=ventas, total_ventas=total_ventas, fecha=fecha, periodo=periodo)

@clientes_bp.route('/quitar_pedido', methods=['POST'])
@login_required
def quitar_pedido():
    pedidos_temporales = leer_pedidos_temporales()
    nombre = request.form.get('nombre', '')
    direccion = request.form.get('direccion', '')
    telefono = request.form.get('telefono', '')

    if pedidos_temporales:
        pedidos_temporales.pop()  
        limpiar_pedidos_temporales()  
        for pedido in pedidos_temporales:
            guardar_pedido_temporal(pedido['tamaño'], pedido['ingredientes'], 
                                  pedido['cantidad'], pedido['subtotal'])
        flash("Último pedido quitado.", "success")
    else:
        flash("No hay pedidos para quitar.", "danger")

    return redirect(url_for('clientes.pedido', nombre=nombre, direccion=direccion, telefono=telefono))

@clientes_bp.route('/terminar_pedido', methods=['POST'])
@login_required
def terminar_pedido():
    nombre = request.args.get('nombre') or request.form.get('nombre')
    direccion = request.args.get('direccion') or request.form.get('direccion')
    telefono = request.args.get('telefono') or request.form.get('telefono')
    
    pedidos_temporales = leer_pedidos_temporales()

    if not pedidos_temporales:
        flash("No hay pedidos para terminar.", "danger")
        return redirect(url_for('clientes.pedido'))

    total_pedido = sum(pedido['subtotal'] for pedido in pedidos_temporales)
    nuevo_pedido = Pedidos(
        nombre=nombre, 
        direccion=direccion, 
        telefono=telefono, 
        total_pedido=total_pedido,
        fecha_compra=datetime.datetime.now()
    )
    db.session.add(nuevo_pedido)
    db.session.commit()

    flash(f"Pedido completado. El total a pagar es: ${total_pedido:.2f}", "success")
    limpiar_pedidos_temporales()

    return redirect(url_for('clientes.pedido'))