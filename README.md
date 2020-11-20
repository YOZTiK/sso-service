# Single Sign On Service (SSO)

Este servicio está diseñado para trabajar con cualquier proveedor de servicio en la nube. Para esta documentación únicamente describiremos los pasos para ejecutar y desplegar el servicio desde la Google Services.
Este sistema funciona al 100%, si y solo si, el resto de servicios están operando de manera normal.
Los servicios a los que nos enlazamos son:
- MDM
- Marketing
- App
- Web

Si alguno de los servicios anteriormente listados se encuentra _offline_ entonces las funciones:
- Authentication
- New User
- Recovery Password
- Update Password

No estarán disponibles debido a la falla con esos servicios.
 

## Comenzando 🚀

Requieres de una cuenta de Google para poder usar el servicio de Google Console y asociar una cuenta de pago para el proyecto. 
Esta es la base para usar las herramientas de gservices y poder comenzar con la ejecución. Puedes iniciar el proceso desde aquí:

* [Google Console](https://console.cloud.google.com/?hl=es-419) - Google Console

Te aconsejamos informarte sobre el plan gratuito de Google antes de comenzar:

* [Start running workloads for free](https://cloud.google.com/free) - Free Tier GServices

Cuando hayas terminado con los pasos anteriores deberás crear un nuevo proyecto, para poder compilar y desplegar el servicio. 
En esta liga podrás encontrar información de como poder crear un nuevo proyecto:

* [Create new proyect](https://cloud.google.com/resource-manager/docs/creating-managing-projects) - Free Tier GServices

Mira **Deployment** para conocer como desplegar el proyecto.


### Pre-requisitos 📋

Requieres de tener una [Terminal de Google](https://cloud.google.com/shell/docs/using-cloud-shell#:~:text=Click%20the%20Activate%20Cloud%20Shell,the%20session%20to%20be%20initialized.) abierta para poder ejecutar los comandos e iniciar con el ambiente.

Primero deberás actualizar la información de los paquetes de configuración del sistema con:
```
sudo apt update
```

### Instalación 🔧

Deberás instalar los siguientes paquetes introduciendo cada comando en la consola:
```
sudo apt install python3 python3-dev python3-venv
sudo apt install wget
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
```

Para la configuración de la DB deberás ingresar al panel de IAM y administración en el apartado de cuentas de servicio.
Deberás crear un nueva cuenta de servicio. El rol de esta nueva cuenta de servicio deberá ser propietario u api engine dependiendo del acceso que quyieras que tenga esta nueva cuenta de servicio.
Deberás abrir de nuevo la cuenta que acabas de crear y seleccionar crear clave. Se desplegará una ventana para poder generar y descargar la clave, deberás descargarla con tipo JSON.

Mira [Create a service account](https://developers.google.com/android/management/service-account) para conocer como crear una nueva cuenta de servicio.

Una vez descargando el JSON deberás subirlo desde la consola de google en la carpeta del proyecto.

Mira [Managing files with Cloud Shell](https://cloud.google.com/shell/docs/uploading-and-downloading-files#:~:text=Uploading%20and%20downloading%20files,-You%20can%20upload&text=Within%20your%20Cloud%20Shell%20Editor,%2FUpload%20Files....) para conocer como subir un archivo desde la consola.
 
Posteriormente deberás agregar este archivo como variable de entorno en el path del sistema, ejecutando el comando:
GOOGLE_APPLICATION_CREDENTIALS

Mira [Setting the environment variable](https://cloud.google.com/docs/authentication/getting-started#setting_the_environment_variable) para conocer como agregar el archivo de credenciales a las variables de entorno.

Una vez terminando con la configuración anterior iniciaremos con la descarga de los archivos del repositorio. Ejecuta el siguiente comando en la terminal:
```
git clone https://github.com/YOZTiK/sso-service
```

Esto te creara una carpeta y podrás iniciar con el despliegue o las pruebas locales.

## Ejecutando las pruebas en servidor local ⚙️

_Ahora ejecutaremos los siguientes comandos para tener un entorno de desarrollo ejecutandose desde la consola_
Tendremos que ingresar a la carpeta que se creó tras descargar el repositorio.
```
cd sso-service
```

_Si queremos iniciar el servicio de forma local deberemos ejecutar:_

```
python3 -m venv venv
source venv/bin/activate
```
_Una vez hayamos ejecutado los comandos anteriores para generar el ambiente de ejecución deberemos instalar los requisitos para el servicio:_
```
sudo pip install -r requirements.txt
```

_Por último bastará con ejecutar:_
```
sudo python3 app.py
```
_Esto hará que nuestro servicio se ejecute en localhost. Y nos mostrará el siguiente mensaje en la consola:_
```
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
```

_Deberemos abrir otra pestaña de la consola y tendremos que enviar las peticiones ejecutando el siguiente comando para probar el servicio._
```
curl --header "Content-Type: application/json" --request POST --data '{<json-data>}' http://0.0.0.0:8080/<function-path>
```

Mira [Service Documentation](https://documenter.getpostman.com/view/10987523/TVetcRcV) para conocer como hacer las peticiones al servicio.

## Despliegue 📦

Una vez teniendo el repositorio en la carpeta del proyecto "sso-service" bastará con ejecutar los siguientes comandos en la consola:

 ```
gcloud builds submit --tag gcr.io/<project-id>/sso-service
```
_Para encontrar el project ID deberás ingresar a la información de de tu proyecto desde el dashboard de google console.
Mira [GService Documentation](https://cloud.google.com/resource-manager/docs/creating-managing-projects#identifying_projects) para conocer en dónde encontrar esta información._

Después de haber ejecutado el comando anterior debeás iniciar con el despliegue ejecutando:

```
gcloud run deploy --image gcr.io/<project-id>/sso-service --platform managed
```

Tras ejecutar el comando te parecerán algunas opciones en la consola:



### Analice las pruebas end-to-end 🔩

_Las pruebas se analizaron para cada elemento de funcionalidad devolviendo resultados exitosos de conexión entre el resto de servicios_

Mira [Service Documentation](https://documenter.getpostman.com/view/10987523/TVetcRcV) para ejecutar pruebas al servicio.

**Los URL de las pruebas se deben modificar dependiendo de en donde se encuentre el servicio** 

### Y las pruebas de estilo de codificación ⌨️

Velocidad y confiabilidad

La prueba de _Authentication_ se ejecutan enviando una petición curl. Encapsulando los parametros dentro del body de un json a un URL similar a este:
 
```
https://<service-url>/<function>
```
Mira [Service Documentation](https://documenter.getpostman.com/view/10987523/TVetcRcV) para visualizar nuestras pruebas en nuestro servicio.

**El URL puede cambiar dependiendo de en donde se encuentre el servicio** 

## Construido con 🛠️

_Las herramientas usadas para crear este proyecto_

* [Pycharm](https://www.jetbrains.com/es-es/pycharm/) - El IDE usado
* [Python3](https://docs.python.org/3/) - El framework usado
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - El framework usado para el despliegue web
* [Git](https://git-scm.com/doc) - Usado para manejar el versionamiento

También puedes mirar la lista de todos los [requisitos](requirements.txt) de este proyecto.

## Contribuyendo 🖇️

Por favor lee el [CONTRIBUTING.md](https://gist.github.com/villanuevand/xxxxxx) para detalles de nuestro código de conducta, y el proceso para enviarnos pull requests.

## Autores ✒️

_Este proyecto fue creado desde sus inicios por:_

* **Yoltic Cervantes Galeana** - *Trabajo Inicial y Documentación* - [YOZTiK](https://github.com/YOZTiK)
* **Luis Angel Diaz Rebollo** - *Diseño de DB y Documentación del Servicio* - [LuisADR18](https://github.com/LuisADR)

También puedes mirar la lista de todos los [contribuyentes](https://github.com/YOZTiK/sso-service/contributors) quíenes han participado en este proyecto. 

## Licencia 📄

Este proyecto está bajo la Licencia MIT - mira el archivo [LICENSE.md](LICENSE.md) para detalles

## Expresiones de Gratitud 🎁

* Gracias virtuales a nuestro profesor que nos apoyo durante la creación de todo el proyecto 📢



---
⌨️ con ❤️ por [YOZTiK](https://github.com/YOZTiK) 😊
