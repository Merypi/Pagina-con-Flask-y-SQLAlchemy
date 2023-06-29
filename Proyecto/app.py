from datetime import datetime
from flask import Flask, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from password import PasswordVer

app = Flask(__name__)
app.config.from_pyfile('config.py')

from models import db 
from models import Estudiante, Curso, Asistencia, Padre, Preceptor
from datetime import datetime
		
@app.route('/')
def inicio():
	return render_template('inicio.html')	

@app.route('/iniciopadre')
def iniciopadre():
	return render_template('inicioPadre.html')

@app.route('/iniciopreceptor')
def iniciopreceptor():
	return render_template('inicioPreceptor.html')

@app.route('/loginpadre', methods = ['GET','POST'])
def loginpadre():  
	if request.method == 'POST': 
		if not request.form['emailPadre'] or not request.form['passwordPadre']:
			return render_template('inicioPadre.html')
		else:
			usuario_padre = Padre.query.filter_by(correo= request.form['emailPadre']).first()
			if usuario_padre is None: #si no encuentra el usuario
				return render_template('inicioPadre.html', error="El correo no está registrado")
			else:
				verificacion = PasswordVer(request.form['passwordPadre'])
				if verificacion.validarPassword(usuario_padre.clave) :                    
					return render_template('menuPadre.html', usuario = usuario_padre)
				else:
					return render_template('inicioPadre.html', error="La contraseña no es válida")

@app.route('/loginpreceptor', methods = ['GET','POST'])
def loginpreceptor():  
	if request.method == 'POST': 
		if not request.form['emailPreceptor'] or not request.form['passwordPreceptor']:
			return render_template('inicioPreceptor.html')
		else:
			usuario_preceptor = Preceptor.query.filter_by(correo= request.form['emailPreceptor']).first()
			if usuario_preceptor is None: #si no encuentra el usuario
				return render_template('inicioPreceptor.html', error="El correo no está registrado")
			else:	
				verificacion = PasswordVer(request.form['passwordPreceptor'])
				if verificacion.validarPassword(usuario_preceptor.clave):       
					session["idpreceptor"]=usuario_preceptor.id             
					return render_template('menuPreceptor.html', usuario = usuario_preceptor)
				else:
					return render_template('inicioPreceptor.html', error="La contraseña no es válida")

@app.route('/registrar_asistencia')
def registrar_asistencia(): 
	preceptorActual=Preceptor.query.filter(Preceptor.id==session["idpreceptor"]).first()
	return render_template('Seleccionar_Fecha.html', prece=preceptorActual)
	
# @app.route('/registrar_asistencia')
# def registrar_asistencia():
#     preceptor_actual = obtener_preceptor_actual()
#     if not preceptor_actual:
#         return redirect(url_for('login'))

#     curso_id = request.args.get('curso_id', None)
#     if not curso_id: 
#         return redirect(url_for('home'))

#     curso = Curso.query.filter_by(id=curso_id, idpreceptor=preceptor_actual.id).first()
#     if not curso:
#         return redirect(url_for('home'))
    
#     if request.method == 'POST':
#         clase = int(request.form['clase'])
#         fecha = request.form['fecha']
#         for estudiante in curso.estudiantes:
#             asistencia = request.form[f'asistencia_{estudiante.id}']
#             justificacion = request.form.get(f'justificacion_{estudiante.id}', '')
#             registro_asistencia = Asistencia(
#                 estudiante_id=estudiante.id,
#                 fecha=fecha,
#                 clase=clase,
#                 asistencia=asistencia,
#                 justificacion=justificacion if asistencia == 'n' else ''
#             )
#             db.session.add(registro_asistencia)
#         db.session.commit()
#         return redirect(url_for('home'))
    
#     estudiantes = Estudiante.query.filter_by(idcurso=curso_id).order_by(Estudiante.nombre, Estudiante.apellido).all()
#     return render_template('registrar_asistencia.html', curso=curso, estudiantes=estudiantes)

@app.route('/nuevaAsistencia', methods = ['GET','POST'])
def nuevaAsistencia():
	if request.method == 'POST':
		if  not request.form['idcurso'] or not request.form['clase']:
			return render_template('error.html', error="Por favor ingrese los datos requeridos")
		else:
			session['tipoclase'] = int(request.form['clase'])
			session['datechose'] = request.form['fecha']
			curso=request.form['idcurso']
			session['cursoselec'] = curso
			cursoactual= Curso.query.filter_by(id=curso).first() #me devuelve el objeto
			estudiantes= Estudiante.query.filter_by(idcurso = cursoactual.id).order_by(Estudiante.apellido, Estudiante.nombre).all()
			longitud=range(len(estudiantes))
			return render_template('Registrar_Alumnos.html', estudiantes=estudiantes, longitud=longitud)

@app.route('/Asistencia_generada', methods = ['GET','POST'])
def Asistencia_generada():
	if request.method == 'POST':
		date= session.get("datechose")
		clase= session.get("tipoclase")
		curso = Curso.query.filter_by(id=session['cursoselec']).first()
		estudiantes = Estudiante.query.filter_by(idcurso = curso.id).order_by(Estudiante.apellido, Estudiante.nombre).all()
		for i in range(len(estudiantes)):
			asis=request.form[f'asistio{i}']
			just=request.form.get(f'justificacion{i}',"")
			nuevoregistro=Asistencia(fecha=datetime.strptime(date, "%Y-%m-%d").date(), codigoclase=clase, asistio=asis, justificacion=just ,idestudiante=estudiantes[i].id )
			db.session.add(nuevoregistro)
		db.session.commit()

		return render_template('Registro_exitoso.html')

@app.route('/generar_listado')
def generar_listado():
	preceptorActual=Preceptor.query.filter(Preceptor.id==session["idpreceptor"]).first()
	return render_template('elegir_cursos.html', prece=preceptorActual)

@app.route('/Mostrar_listado', methods = ['POST'])
def Mostrar_listado():
	listado=[]
	if request.method== 'POST':
		idcurso = request.form['idcurso'] 
		curso= Curso.query.filter_by(id=idcurso).first() #me devuelve el objeto
		estudiantes= Estudiante.query.order_by(Estudiante.apellido, Estudiante.nombre).all()

		for estudiante in estudiantes:
			if estudiante.idcurso == curso.id:
				aulaPresente = 0
				aulaJustificada = 0
				aulaInjustificada = 0
				edfPresente = 0
				edfJustificada = 0
				edfInjustificada = 0
				total= 0.0
				asistencias = Asistencia.query.filter_by(idestudiante=estudiante.id).all()
				for asistencia in asistencias:
					if asistencia.codigoclase == 1:
						if asistencia.asistio == 's':
							aulaPresente += 1
						else: 
							if asistencia.justificacion == None: 
								aulaInjustificada += 1
							else:
								aulaJustificada += 1
							total +=1
					else:
						if asistencia.asistio == 'n':
							if asistencia.justificacion == None:
								edfInjustificada +=1
							else:
								edfJustificada +=1
							total += 0.5
						else:
							edfPresente += 1
						
					info_asistencia = {
                    'apellido': estudiante.apellido,
                    'nombre': estudiante.nombre,
                    'aula_presentes': aulaPresente,
                    'aula_justificadas': aulaJustificada,
                    'aula_Injustificadas':aulaInjustificada,
		    		'ef_presentes': edfPresente,
                    'ef_justificadas':edfJustificada,
                    'ef_Injustificadas':edfInjustificada,
                    'total':total
                    }
				listado.append(info_asistencia)
							
		return render_template('informeDetallado.html', curso=curso, listado=listado)
         

if __name__ == '__main__':
	    app.run(debug = True)
