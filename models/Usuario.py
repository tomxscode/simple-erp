from . import login_manager, db
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
  return Usuario.query.get(user_id)

class Usuario(db.Model, UserMixin):
  run = db.Column(db.String(10), primary_key=True)
  email = db.Column(db.String(50), unique=True, nullable=False)
  pin = db.Column(db.String(128), nullable=False)
  nombre = db.Column(db.String(50), nullable=False)
  apellido = db.Column(db.String(50), nullable=False)
  rol = db.Column(db.Integer, nullable=False)
  estado = db.Column(db.Integer, nullable=False)
  telefono = db.Column(db.String(20), nullable=True)
  
  def get_id(self):
    return self.run