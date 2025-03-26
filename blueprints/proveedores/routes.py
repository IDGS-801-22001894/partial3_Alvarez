from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models import Proveedor, User
from forms import ProveedorForm, ModificarProveedorForm

proveedores_bp = Blueprint('proveedores', __name__, template_folder='templates')

@proveedores_bp.route('/proveedores')
@login_required
def proveedores():
    # Verificar que el usuario sea proveedor
    if current_user.role != 'proveedor':
        flash('Acceso restringido a proveedores', 'danger')
        return redirect(url_for('clientes.pedido'))
    
    # Mostrar todos los proveedores no eliminados
    proveedores = Proveedor.query.filter_by(eliminado=False).all()
    return render_template('proveedores.html', proveedores=proveedores)

@proveedores_bp.route('/registrar_proveedor', methods=['GET', 'POST'])
@login_required
def registrar_proveedor():
    # Solo proveedores pueden registrar
    if current_user.role != 'proveedor':
        flash('Acceso restringido', 'danger')
        return redirect(url_for('clientes.pedido'))

    form = ProveedorForm()
    if form.validate_on_submit():
        try:
            # Verificar si el usuario ya existe
            if User.query.filter_by(username=form.nombre.data).first():
                flash('Nombre de usuario ya registrado', 'danger')
                return redirect(url_for('proveedores.registrar_proveedor'))

            # Crear usuario con rol proveedor
            usuario = User(
                username=form.nombre.data,
                password=form.password.data,
                role='proveedor'
            )
            db.session.add(usuario)
            db.session.commit()
            
            # Crear perfil de proveedor
            proveedor = Proveedor(
                nombre=form.nombre.data,
                direccion=form.direccion.data,
                correo=form.correo.data,
                calle=form.calle.data,
                telefono=form.telefono.data,
                user_id=usuario.id
            )
            db.session.add(proveedor)
            db.session.commit()
            
            flash('Proveedor registrado exitosamente', 'success')
            return redirect(url_for('proveedores.proveedores'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar: {str(e)}', 'danger')
    
    return render_template('registrar_proveedor.html', form=form)

@proveedores_bp.route('/modificar_proveedor/<int:id>', methods=['GET', 'POST'])
@login_required
def modificar_proveedor(id):
    # Solo proveedores pueden modificar
    if current_user.role != 'proveedor':
        flash('Acceso restringido', 'danger')
        return redirect(url_for('clientes.pedido'))
    
    proveedor = Proveedor.query.get_or_404(id)
    usuario = User.query.get_or_404(proveedor.user_id)
    
    form = ModificarProveedorForm(obj=proveedor)
    
    if form.validate_on_submit():
        try:
            # Verificar si el nuevo nombre ya está en uso
            if Proveedor.query.filter(
                Proveedor.nombre == form.nombre.data, 
                Proveedor.id != id,
                Proveedor.eliminado == False
            ).first():
                flash('Nombre ya en uso por otro proveedor', 'danger')
                return redirect(url_for('proveedores.modificar_proveedor', id=id))

            # Actualizar datos del proveedor
            proveedor.nombre = form.nombre.data
            proveedor.direccion = form.direccion.data
            proveedor.correo = form.correo.data
            proveedor.calle = form.calle.data
            proveedor.telefono = form.telefono.data
            
            # Actualizar nombre de usuario asociado
            usuario.username = form.nombre.data
            
            db.session.commit()
            flash('Proveedor actualizado exitosamente', 'success')
            return redirect(url_for('proveedores.proveedores'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}', 'danger')
    
    return render_template('modificar_proveedor.html', form=form, proveedor=proveedor)

@proveedores_bp.route('/eliminar_proveedor/<int:id>', methods=['POST'])
@login_required
def eliminar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    usuario = User.query.get(proveedor.user_id)
    
    try:
        db.session.delete(proveedor)
        db.session.delete(usuario)
        db.session.commit()
        flash('Proveedor eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar proveedor: {str(e)}', 'danger')
    
    return redirect(url_for('proveedores.proveedores'))