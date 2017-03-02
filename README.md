##Despliegue de una aplicación Python en heroku.

Este documento recoje los pasos que he seguido para hacer el despliegue de mi aplicación. Antes de empezar decir que mi aplicación esta hecha con el microfraemwork Flask y con python 3. Para el despliegue he utilizado el PaaS Heroku. 

-Teniendo la aplicación lista es decir, si por ejemplo si yo ejecuto  esto “python3 nombre_app.py “ la aplicación se lanza  localmente de forma correcta. Entonces podemos empezar.

Pasos:

1- Como voy a utilizar Heroku para el despliegue necesito hacer con este varias cosas. La primera es registrarse en la web de Heroku y ahi crear una apliacacíon. Le damos el nombre que queramos y ya tenemos en heroku un “espacio” creado para nuestra apliación.

2-Heroku tiene una interfaz de lina de comandos llamada (Heroku CLI), que basicamente lo que hace o podemos hacer es interatuar con heroku. Por ejemplo hacer login con nuestra cuenta que antes hemos creado. Para  instalar esta interfaz con la orden “sudo apt-get install heroku”, nos basta para tener ya en local esta interfaz de comandos.  Verificamo la instalación con la orden “heroku –-version”. 

3-Con estos dos pasos ya tenemos la parte de heroku lista.  Ahora necesitamos crear dentro del directorio de nuestra apliación dos ficheros. Uno es “runtime.txt”, este fichero es muy importante tenerlo ya que con el lo que vamos hacer es decirle a heroku la versión de python que queremos utilizar para el despliegue. En mi caso este fichero contiene “python-3.6.0”. Tembién necesitamos crear un fichero llamado “Procfile”.  En este fichero sirve para que heroku sepa como lanzar la aplicación.  En concreto se utiliza un servico HTTP con es “Gunicorn” (Python WSGI HTTP Server for Unix).  De tal forma que cuando se solicite una petición gunicorn se la pasará a Flask y este respondera lo solicitado.  Mi Fichero procfile contiene lo siguiente:  “web gunicorn nombre_app:app”. Que hace que lanze la aplicación, por eso hay que especificarle el módulo principal de la apliación y la variable que vamos a usar para lanzar, es decir la llamada a app. Por último necesitamos saber las versiones de todo lo que utiliza nuestra apliación. Es decir que requiere nuestra apliación para que haga el despliegue correctamente.  Para ello tenemos el fichero “requirements.txt”.  Con la orden “pip3 freeze >> requirements.txt ”, Metemos en el fichero todo lo que requiere nuestra aplaición.

4-Mi aplaición utiliza como base de datos “MongoDB”. Entonces a heroku hay que decirle que vamos utilizar esta. Desde la linea de ordenes de heroku añadimos el “addons” necesario que es “mongohq”. Y ahora si ejecutamos la siguiente orden “heroku  config”. Obtendremos  el id de la base de datos de mongo en heroku. Esto junto con la variable MONGOHQ_URL lo debemos de poner en el fichero principal de la aplicación. Para que cuando esta se ejeucte funcione bien cuando interactue con la base de datos detro de heroku.

5-Ya tenemos todo listo para subir la aplicación a heroku. Lo siguiente es crear el repositorio de heroku con “heroku create”. Para hacer la subida de los ficheros y carpetas de nuestra apliación vamos a utilizar git. Entonces previamente añadiendo los repositorios remotos de nuestra apliación en heroku. Con “git add ficheros” preparamos lo que vamos a subir. Hacemos un commit, y con la orden “git push heroku master” heroku comenzará a desplegar la aplaición. Si todo es correcto heroku al final nos dice la url para poder acceder a nuesrtra apliación ya desplegada. 



Mi apliación: https://lawapp.herokuapp.com/index 

