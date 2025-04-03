API de Reporte de Incidentes

Tecnologías
Python
Flask
PostgreSQL

1.	Crear entorno virtual:
python -m venv venv
venv\Scripts\activate

3.	Instalar librerías:
pip install flask flask_sqlalchemy psycopg2-binary

5.	Crear base de datos en PgAdmin (nombre: incidentes_db)
   
6.	Cambiar la configuración de la base de datos en app.py:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tu_contraseña@localhost:5432/incidentes_db'

7.	Crear tablas:
python
from app import db, app
with app.app_context():
    db.create_all()
exit()


8.	Ejecutar la API:
python app.py

Reglas de validación:
reporter no puede ir vacío
description debe tener mínimo 10 caracteres
Solo se puede actualizar el campo status

