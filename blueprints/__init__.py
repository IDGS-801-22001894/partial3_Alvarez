from flask import Flask
from flask_login import current_user
from flask import redirect, url_for, flash
from models import Proveedor

def init_app(app: Flask):
    from blueprints.clientes.routes import clientes_bp
    from blueprints.proveedores.routes import proveedores_bp
    from blueprints.login.routes import login_bp
    
    # Registrar blueprints con prefijos
    app.register_blueprint(clientes_bp, url_prefix='/clientes')
    app.register_blueprint(proveedores_bp, url_prefix='/proveedores')
    app.register_blueprint(login_bp, url_prefix='/login')
    
    @app.route('/')
    def index():
        """Redirige al usuario a la página adecuada según su rol"""
        if current_user.is_authenticated:
            # Solo verifica el rol 'proveedor'
            if getattr(current_user, 'role', None) == 'proveedor':
                proveedor = Proveedor.query.filter_by(user_id=current_user.id).first()
                if proveedor:
                    return redirect(url_for('proveedores.proveedores'))
                flash('Tu cuenta no tiene perfil de proveedor asignado', 'danger')
                return redirect(url_for('clientes.pedido'))
            
            # Redirección por defecto para clientes
            return redirect(url_for('clientes.pedido'))
        
        # Usuario no autenticado
        return redirect(url_for('login.login'))

    @app.errorhandler(404)
    def page_not_found(e):
        flash('Página no encontrada', 'danger')
        return redirect(url_for('index'))