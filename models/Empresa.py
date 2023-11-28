from . import db

class Empresa(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nombre = db.Column(db.String(100), nullable=False)
  direccion = db.Column(db.String(100), nullable=False)
  telefono = db.Column(db.String(20), nullable=False)
  email = db.Column(db.String(100), nullable=False)
  rut = db.Column(db.String(22), nullable=False)