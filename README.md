# Paises que más tuitean sobre el Coronavirus


#### Alberto Martín Núñez

## Indice de contenidos

1. [Objetivo de la práctica](#id1)
2. [Aplicación PySpark](#id2)
    1. [Metodología y datos obtenidos](#id2.1)
    2. [Visualización de los datos](#id2.2)
3. [Conclusiones](#id4)


### Objetivo de la práctica <a name="id1"></a>

El objetivo de esta práctica consistía en plantear un problema a resolver utilizando **Spark Streaming**.

Como problema a resolver he propuesto conocer cuales son los paises que Tuitean más sobre el coronavirus. Tras la situación que estamos sufriendo en el planeta sobre las pandemia por el Covid-19, se plantea averiguar cuales son los países que actualmente estan *Tuiteando* más sobre esta tragedia. A través de esta información podríamos averiguar aspectos sobre esos países y la situación que estan viviendo, ya que la afluencia de hablar sobre el Covid-19 puede traer consigo información valiosa del estado de ese país.

### Aplicación PySpark <a name="id2"></a>

Ahora pasaré a detallar la aplicación PySpark que se ha realizado para afrontar el problema descrito anteriormente.

#### Metodología y datos obtenidos <a name="id2.1"></a>

Esta parte de la práctica se ha desarrollado en dos ficheros: *tweet_data.py* y *spark.py*

##### tweet_data.py

En este fichero consiste en recoger los tweets de Twitter para después enviarselo por una conexion tcp a nuestro *spark.py* que se encargará del procesamiento de los datos.

Esto lo hacemos de la siguiente forma:

- Obtención de Tweets
  
![Obtencion de tweets](img/tweets.jpeg)

Creamos la *query* con la palabra clave *'covid'* y las credenciales que se obtienen al registrarse en **TwitterApps** para poder obtener los Tweets.

Estas credenciales estan en un fichero a parte que se llama *credentials* que no se ha incluido en el repositorio.

- Envío de Tweets a nuestro *sparkstreaming*ç
![Tweets to Spark](img/tweet_spark.jpeg)

Aora cogemos la respuesta que nos da la funcion anterior y parseamos el *json* que nos devuelve y nos quedamos con el código del pais y estos los enviamos por una conexion TCP.

- Creación de la conexión
 
```python
TCP_IP = 'localhost'
TCP_PORT = 5556
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((TCP_IP, TCP_PORT))
s.listen(1)

print("Esperando por la conexion")
conn, addr = s.accept()
print('------------------------')
print("Conectados, busquemos los paises que más hablan sobre el coronavirus")

resp = ReadTweets()
TweetsToSpark(resp, conn)

```


##### spark.py

#### Visualización de los datos <a name="id2.2"></a>

### Visualización de los datos <a name="id3"></a>