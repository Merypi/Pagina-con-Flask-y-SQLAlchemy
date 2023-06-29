from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy(app)

class Curso(db.Model):
    __tablename__= 'curso'
    id = db.Column(db.Integer, primary_key=True)
    anio = db.Column(db.Integer, nullable=False)
    division = db.Column(db.Integer, unique=True, nullable=False)
    estudiantes = db.relationship('Estudiante',backref='curso',uselist=False, cascade='all, delete-orphan')
    idpreceptor =  db.Column(db.Integer, db.ForeignKey('preceptor.id'))
	
class Asistencia(db.Model):
    __tablename__= 'asistencia'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    codigoclase = db.Column(db.Integer, primary_key=True)
    asistio = db.Column(db.String(80), nullable=False )
    justificacion = db.Column(db.String(150),  nullable=False)
    idestudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id'))

class Estudiante(db.Model):
    __tablename__= 'estudiante'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    dni = db.Column(db.String(80), nullable=False)
    idcurso= db.Column(db.Integer, db.ForeignKey('curso.id'))
    idpadre = db.Column(db.Integer, db.ForeignKey('padre.id'))
    asistencia= db.relationship('Asistencia',backref='Estudiante', cascade='all, delete-orphan')

class Padre(db.Model):
    __tablename__ = 'padre'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    clave = db.Column(db.String(100), nullable=False)
    estudiantes = db.relationship('Estudiante',backref='padre',uselist=False, cascade='all, delete-orphan')

class Preceptor(db.Model):
    __tablename__= 'preceptor'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    clave = db.Column(db.String(120), unique=False, nullable=False)
    curso = db.relationship('Curso', backref='preceptor', cascade='all, delete-orphan')
   
   