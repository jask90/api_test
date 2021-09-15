# API con Django REST Framework

Para levantar el proyecto únicamente necesita tener instalado docker en su equipo.

Teniendo el repositorio clonado y estando posicionado en la raiz del proyecto crearemos la imagen de docker:
> docker build -t df_drf .

Con la imagen creada procedemos a crear el contenedor:
> docker run -d -p 8000:8000 --name df_drf df_drf

Esto nos dejará un contenedor levantado, si queremos acceder al mismo podemos hacerlo con el comando:
> docker exec -ti df_drf bash

# Ejecutar tests

Una vez dentro del contenedor podemos lanzar los tests unitarios con el siguiente comando:
> python3 /opt/api_test/df_drf/manage.py test cars
Esto ejecuta los tests ubicados en el directorio '/opt/api_test/df_dr/cars/tests/'.

# Características del proyecto
Cuenta con dos endpoints (carbrands/ y carmodels/) que permiten la creación, modificación, elimitación y obtención de los objetos de los modelos Car y Brand de la base de datos.

Este proyecto está Dockerizado, cuenta con test unitarios para las funcionalidades principales de los modelos antes mencionados, y se ha implementado la posibilidad de utilizar OAuth2 en las peticiones a la API.

Se han adjuntado unos fixtures para poblar mínimamente la base de datos y poder probar todas las funcionalidades de manera inmediata.
En estos fixtures se incluyen dos usuarios con sus contraseñas:
* admin / 123456: Usuario administrador
* api_user / cyPNjhx9aNADjF4Z: Usuario api preparado para utilizar con OAuth2

Los datos para utilizar OAuth2 con el usuario api_user se pueden encontrar en: /admin/oauth2_provider/application/1/change/
