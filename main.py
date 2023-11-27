from flask import Flask
from models import db, login_manager

app = Flask(__name__)
app.secret_key = "Xxxxxx"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db.init_app(app)
login_manager.init_app(app)

from routes.usuario import usuario

app.register_blueprint(usuario)

with app.app_context():
  db.create_all()

if __name__ == '__main__':
  app.run(debug=True)