from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from db import db
from utils import validations
import os
import json
from datetime import datetime
app = Flask(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))
upload_dir = os.path.join(current_dir, 'static', 'photos')
app.config['UPLOAD_FOLDER'] = upload_dir

@app.route('/')
def index():
    # Obtener los datos de las últimas donaciones y pedidos desde la base de datos
    last_donations = db.obtener_donaciones(1)
    last_pedidos = db.obtener_pedidos(1)
    ped = []
    don = []
    for donaciones in last_donations:
        comuna_n = db.nombre_comuna(donaciones['comuna_id'])
        date = donaciones['fecha_disponibilidad'].strftime("%m/%d/%Y")
        d_dict = {'id': donaciones['id'], 'calle_numero': donaciones['calle_numero'], 'tipo': donaciones['tipo'], 
                  'cantidad': donaciones['cantidad'], 'email': donaciones['email'], 
                  'comuna': comuna_n[0], 'fecha': date}
        don.append(d_dict)
    for pedidos in last_pedidos:
        comuna_n = db.nombre_comuna(pedidos[1])
        p_dict = {'id': pedidos[0], 'tipo': pedidos[2], 'cantidad': pedidos[4], 
                  'email': pedidos[6], 'comuna': comuna_n[0]}
        ped.append(p_dict)
    donations_json = json.dumps(don)
    pedidos_json = json.dumps(ped)
    return render_template('inicio.html', donations=donations_json, pedidos=pedidos_json)

@app.route('/agregar-donacion', methods=['GET', 'POST'])
def agregar_donacion():
    ty_msg = False
    back_btn = False
    if request.method == 'POST':
        # Obtener los datos del formulario
        comuna = request.form.get('comuna')
        calle = request.form.get('calle-numero')
        tipo = request.form.get('tipo')
        cantidad = request.form.get('cantidad')
        descripcion = request.form.get('descripcion')
        condiciones = request.form.get('condiciones')
        img = request.files['files']
        name = request.form.get('nombre')
        email = request.form.get('email')
        phone_number = request.form.get('telefono')
        date = request.form.get('fecha-disponibilidad')

        # Validar el formulario
        if validations.validate_donation_form(calle, tipo, cantidad, descripcion, condiciones, img, name, email, phone_number, date):
            # Llamar a la función insert_donation para insertar la donación en la base de datos
            donacion_id = db.insert_donation(comuna, calle, tipo, cantidad, date, descripcion, condiciones, name, email, phone_number)
            if 'files' in request.files:
                fotos = request.files.getlist('files')
                for foto in fotos:
                    if foto:
                        nombre_archivo = secure_filename(foto.filename)
                        ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
                        foto.save(ruta_archivo)
                        db.insert_foto(ruta_archivo, nombre_archivo, donacion_id)
                        ty_msg = True
                        back_btn = True
        else:
            # Renderizar el formulario nuevamente con mensajes de error
            return render_template('agregar-donacion.html', error_message='Hubo un error en la validación del formulario.')

    # Si es una solicitud GET o si no se han enviado datos del formulario
    # renderizar el formulario vacío sin mensaje de error
    return render_template('agregar-donacion.html', error_message=None, ty_msg=ty_msg, back_btn=back_btn)

@app.route('/agregar-pedido', methods=['GET', 'POST'])
def agregar_pedido():
    ty_msg = False
    back_btn = False
    if request.method == 'POST':
        # Obtener los datos del formulario
        comuna = request.form.get('comuna')
        tipo = request.form.get('tipo')
        descripcion = request.form.get('descripcion')
        cantidad = request.form.get('cantidad')
        name = request.form.get('nombre')
        email = request.form.get('email')
        phone_number = request.form.get('telefono')

        if validations.validate_pedido_form(tipo, descripcion, cantidad, name, email, phone_number):
            # Llamar a la función insert_pedido para insertar la donación en la base de datos
            db.insert_pedido(comuna, tipo, descripcion, cantidad, name, email, phone_number)
            ty_msg = True
            back_btn = True
        else:
            # Renderizar el formulario nuevamente con mensajes de error
            return render_template('agregar-pedido.html', error_message='Hubo un error en la validación del formulario.')

    # Si es una solicitud GET o si no se han enviado datos del formulario
    # renderizar el formulario vacío sin mensaje de error
    return render_template('agregar-pedido.html', error_message=None, ty_msg=ty_msg, back_btn=back_btn)

@app.route('/ver-donaciones', methods=['GET'])
def ver_donaciones():
    page = request.args.get('page', 1, type=int)
    donaciones = db.obtener_donaciones(page) 
    return render_template('ver-donaciones.html', donaciones=donaciones, page=page)

@app.route('/informacion-donacion')
def informacion_donacion():
    id_donacion = request.args.get('id')
    donacion = db.obtener_donacion_por_id(id_donacion)
    return render_template('informacion-donacion.html', donation=donacion[0])

@app.route('/ver-pedidos', methods=['GET'])
def ver_pedidos():
    page = request.args.get('page', 1, type=int)
    pedidos = db.obtener_pedidos(page)
    return render_template('ver-pedidos.html', pedidos=pedidos, page=page)

@app.route('/informacion-pedido')
def informacion_pedido():
    id_pedido = request.args.get('id')
    pedido = db.obtener_pedido_por_id(id_pedido)
    return render_template('informacion-pedido.html', pedido=pedido)

@app.route('/estadisticas')
def estadisticas():
    donations = db.cant_donaciones()
    pedidos = db.cant_pedidos()
    ped = []
    don = []
    for donacion in donations:
        d_dict = {'tipo': donacion[0], 'cantidad': donacion[1]}
        don.append(d_dict)
    for pedido in pedidos:
        p_dict = {'tipo': pedido[0], 'cantidad': pedido[1]}
        ped.append(p_dict)
    donations_json = json.dumps(don)
    pedidos_json = json.dumps(ped)
    return render_template('estadisticas.html', donations = donations_json, pedidos = pedidos_json)

if __name__ == '__main__':
    app.run(debug=True)
