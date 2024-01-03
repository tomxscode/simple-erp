from . import db

class Empleado(db.Model):
    rut = db.Column(db.String(12), primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(10), nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    fecha_ingreso = db.Column(db.Date, nullable=False)
    estado = db.Column(db.Boolean, nullable=False)