from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from extensions import db, login_manager
from models import User
from blueprints import init_app

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'

    csrf = CSRFProtect()
    csrf.init_app(app)
    
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'
    
    db.init_app(app)

    init_app(app)

    return app

app = create_app()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3000)