from flask import Blueprint
from extensions import db
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from models import User, Proveedor
from forms import LoginForm

login_bp = Blueprint('login', __name__, template_folder='../../../templates')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('clientes.pedido'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            
            # Verificación mejorada
            if user.role == 'proveedor':
                proveedor = Proveedor.query.filter_by(user_id=user.id).first()
                if proveedor:
                    flash('Bienvenido proveedor', 'success')
                    return redirect(url_for('proveedores.proveedores'))
                else:
                    flash('Tu cuenta no tiene un perfil de proveedor asignado', 'warning')
                    return redirect(url_for('clientes.pedido'))
            else:
                flash('Bienvenido cliente', 'success')
                return redirect(url_for('clientes.pedido'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html', form=form)

@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('login.login'))