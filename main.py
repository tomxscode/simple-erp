from flask import Flask
from models import db, login_manager

app = Flask(__name__)
app.secret_key = "Xxxxxx"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'usuario.login'
login_manager.login_message = 'Necesitas iniciar sesión para realizar esta acción'
login_manager.login_message_category = 'error'

from routes.usuario import usuario
from routes.empresa import empresa

app.register_blueprint(usuario)
app.register_blueprint(empresa)

with app.app_context():
  db.create_all()

if __name__ == '__main__':
  app.run(debug=True)