import pymysql

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8"

def get_conn():
	conn = pymysql.connect(
		db=DB_NAME,
		user=DB_USERNAME,
		passwd=DB_PASSWORD,
		host=DB_HOST,
		port=DB_PORT,
		charset=DB_CHARSET
	)
	return conn

def insert_foto(ruta_archivo, nombre_archivo, donacion_id):
    connection = get_conn()
    cursor = connection.cursor()

    sql = """
    INSERT INTO foto (ruta_archivo, nombre_archivo, donacion_id) 
    VALUES (%s, %s, %s)
    """

    cursor.execute(sql, (ruta_archivo, nombre_archivo, donacion_id))

    connection.commit()

    cursor.close()
    connection.close()

def insert_donation(comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular):
    connection = get_conn()
    cursor = connection.cursor()

    sql = """
    INSERT INTO donacion (comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular))

    donacion_id = cursor.lastrowid

    connection.commit()

    cursor.close()
    connection.close()

    return donacion_id
    
def insert_pedido(comuna_id, tipo, descripcion, cantidad, nombre, email, celular):
    connection = get_conn()
    cursor = connection.cursor()

    sql = """
    INSERT INTO pedido (comuna_id, tipo, descripcion, cantidad, nombre_solicitante, email_solicitante, celular_solicitante)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (comuna_id, tipo, descripcion, cantidad, nombre, email, celular))

    connection.commit()

    cursor.close()
    connection.close()

def obtener_donaciones(page):
    connection = get_conn()
    cursor = connection.cursor()

    per_page = 5
    offset = (page - 1) * per_page

    sql = """
    SELECT donacion.id, comuna_id, tipo, cantidad, fecha_disponibilidad, nombre, calle_numero, email, GROUP_CONCAT(foto.nombre_archivo) as fotos
    FROM donacion
    LEFT JOIN foto ON donacion.id = foto.donacion_id
    GROUP BY donacion.id
    ORDER BY donacion.id DESC
    LIMIT %s OFFSET %s
    """

    cursor.execute(sql, (per_page, offset))
    donaciones = cursor.fetchall()

    cursor.close()
    connection.close()

    donaciones_con_fotos = []
    for donacion in donaciones:
        fotos = donacion[8]  # El campo de fotos es el séptimo campo
        if fotos is not None:
            fotos = fotos.split(',')  # Separar las rutas de las fotos
        donacion_dict = {'id': donacion[0], 'comuna_id': donacion[1], 'tipo': donacion[2], 'cantidad': donacion[3],
                         'fecha_disponibilidad': donacion[4], 'nombre': donacion[5], 'fotos': fotos, 
                         'calle_numero': donacion[6], 'email': donacion[7]}
        donaciones_con_fotos.append(donacion_dict)

    return donaciones_con_fotos


def obtener_donacion_por_id(id_donacion):
    connection = get_conn()
    cursor = connection.cursor()

    sql = """
    SELECT donacion.id, comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, donacion.nombre, email, celular, 
    GROUP_CONCAT(foto.nombre_archivo) as fotos, region.nombre as nombre_region, comuna.nombre as nombre_comuna
    FROM donacion
    LEFT JOIN foto ON donacion.id = foto.donacion_id
    INNER JOIN comuna ON donacion.comuna_id = comuna.id
    INNER JOIN region ON comuna.region_id = region.id
    WHERE donacion.id = %s
    """

    cursor.execute(sql, (id_donacion,))
    donaciones = cursor.fetchall()

    cursor.close()
    connection.close()

    donaciones_con_fotos = []
    for donacion in donaciones:
        fotos = donacion[11]
        if fotos is not None:
            fotos = fotos.split(',')  # Separar las rutas de las fotos
        donacion_dict = {'id': donacion[0], 'comuna_id': donacion[1], 'calle_numero': donacion[2], 'tipo': donacion[3],
                         'cantidad': donacion[4], 'fecha_disponibilidad': donacion[5], 'descripcion': donacion[6], 
                         'condiciones_retirar': donacion[7], 'nombre': donacion[8], 'email': donacion[9], 
                         'celular': donacion[10], 'fotos': fotos, 'nombre_region': donacion[12],
                         'nombre_comuna': donacion[13]}
        donaciones_con_fotos.append(donacion_dict)

    return donaciones_con_fotos

def obtener_pedidos(page):
    connection = get_conn()
    cursor = connection.cursor()

    per_page = 5
    offset = (page - 1) * per_page

    sql = """
    SELECT id, comuna_id, tipo, descripcion, cantidad, nombre_solicitante, email_solicitante
    FROM pedido 
    ORDER BY id DESC 
    LIMIT %s OFFSET %s
    """

    cursor.execute(sql, (per_page, offset))
    pedidos = cursor.fetchall()

    cursor.close()
    connection.close()

    return pedidos

def obtener_pedido_por_id(id_pedido):
    connection = get_conn()
    cursor = connection.cursor()

    sql = """
    SELECT p.id, p.comuna_id, c.nombre AS nombre_comuna, r.nombre AS nombre_region, p.tipo, p.descripcion, p.cantidad, p.nombre_solicitante, p.email_solicitante, p.celular_solicitante
    FROM pedido p
    JOIN comuna c ON p.comuna_id = c.id
    JOIN region r ON c.region_id = r.id
    WHERE p.id = %s
    """

    cursor.execute(sql, (id_pedido,))
    pedido = cursor.fetchone()

    cursor.close()
    connection.close()

    return pedido

def nombre_comuna(id_comuna):
    connection = get_conn()
    cursor = connection.cursor()

    sql = """
    SELECT nombre FROM comuna
    WHERE id = %s
    """

    cursor.execute(sql, (id_comuna,))
    comuna = cursor.fetchone()

    cursor.close()
    connection.close()

    return comuna

def cant_pedidos():
    connection = get_conn()
    cursor = connection.cursor()

    sql = """
    SELECT tipo, COUNT(*) AS cantidad
    FROM pedido
    GROUP BY tipo;
    """

    cursor.execute(sql)
    pedidos = cursor.fetchall()

    cursor.close()
    connection.close()

    return pedidos

def cant_donaciones():
    connection = get_conn()
    cursor = connection.cursor()

    sql = """
    SELECT tipo, COUNT(*) AS cantidad
    FROM donacion
    GROUP BY tipo;
    """

    cursor.execute(sql)
    donaciones = cursor.fetchall()

    cursor.close()
    connection.close()

    return donaciones