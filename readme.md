**Autor:** Nicolas Caceres Plaza

La tarea consiste en una aplicacion de flask, la cual se puede inicializar corriendo app.py.
El proyecto cuenta con las carpetas db, static, templates y utils.

** En db **

Se asume que se ha creado la base de datos tarea2 en Mysql con el archivo tarea2.sql y se cargan los datos del script region-comuna.sql.
Se uso el archivo db.py para manejar la base de datos, usando pymysql.  

** En Static **

poseemos 4 carpetas:
- js: que contiene los archivos JavaScript usados:
	- region_comunas.js contiene la información de las regiones y sus respectivas comunas, la informacion fue obtenida 
      del archivo JSON subido en material docente. Permite cargar los datos al HTML correspondiente.		
	- validation.js se encarga de realizar todas las validaciones y manejar el submit del form correspondiente a Agregar una donación.
	- validation2.js realiza la misma funcion, pero para Agregar un pedido.
- css: contiene 3 css para el estilo de la pagina web.
- json: contiene un archivo json con la informacion de latiud y longitud de cada comuna.
- photos: carpeta donde se van almacenando las fotos al agregar una donacion.

** En Templates **

Estan todos los html de la tarea 1 adaptados para usar rutas de flask y cumplir con todas las indicaciones de la tarea 2.
Adicionalmente, se agregó estadisticas.html y se modificó inicio.html de acuerdo a lo señalado en la tarea 3.

** En utils **

Se creo un archivo validations.py para manejar las entradas por parte del servidor, como medida de seguridad ante ataques maliciosos.

** Creditos **

- El codigo de validations.js esta inspirado en el usado en el auxiliar 3 del curso.
- El modal usado de confirmacion esta basado en uno provisto en el foro del curso perteneciente a w3schools.
- el codigo de validations.py y db.py esta inspirado en el auxiliar 6 del curso.