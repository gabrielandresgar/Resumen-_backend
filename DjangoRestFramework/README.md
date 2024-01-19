# DjangoRestFramework

## Todo en consola de comandos (cmd, no ejecutar con gitbash o con powershell)  
## El api se encuentra por defecto en la ruta http://127.0.0.1:8000/api/v1/ al iniciar el servidor, para mas aclaraciones consulta la documentación de la api en http://127.0.0.1:8000/docs/  

## Crea un entorno virtual  
python -m venv venv  

## Activa el entorno virtual  
.\venv\Scripts\activate   
(escribe deactivate para salir del entrono virtual o simplemente cierra la terminal) 

## Instala las dependencias en base a requirements.txt  
pip install -r requirements.txt  

## Crea las migraciones a la BD
python manage.py makemigrations api  
python manage.py migrate  

## Ejecuta el servidor  
python manage.py runserver  

## Crear superusuario (opcional)
python manage.py createsuperuser
esto creara un superusuario para la ruta de http://127.0.0.1:8000/admin/
(es una interfaz gráfica donde se pueden agregar datos a la BD directamente, llenar todos los datos que se piden para que se pueda crear, si la contraseña es muy corta y solo esta en entorno local, ignorar la advertencia y decir que quieres continuar de todos modos, en este caso escribir la 'y')