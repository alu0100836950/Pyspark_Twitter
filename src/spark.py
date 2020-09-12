from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext

import sys
import requests
#from pyspark.sql.types import *

import pandas as pd

def aggregate_tags_count(new_values, total_sum):
    return sum(new_values) + (total_sum or 0)

def get_sql_context_instance(spark_context):
    if ('sqlContextSingletonInstance' not in globals()):
            globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
    return globals()['sqlContextSingletonInstance']



def process_rdd(time, rdd):
    print("----------- Nueva informacion -----------" )

    try:
       
        sql_context = get_sql_context_instance(rdd.context)
        
        row_rdd = rdd.map(lambda w: Row(word=w[0], word_count=w[1]))
        
        # creamos el dataframe
        hashtags_df = sql_context.createDataFrame(row_rdd)
        
        # Una vez el dataframe creado creamos una tabla en un contexto sql con un nombre especifico
        sql_context.registerDataFrameAsTable(hashtags_df, "hashtags")
      

        country_counts_df = sql_context.sql("select word as Codigo_Pais, word_count as Num_Tweets from hashtags where word like 'CC%'order by word_count desc limit 5")
        country_counts_df.show()
        country_counts_df.coalesce(1).write.format('com.databricks.spark.csv').mode('overwrite').option("header", "true").csv("/home/alberto/Documentos/Master_informatica/Computacion_en_la_nube/pyspark_twitter/data/country_file.csv")
   
       
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)



# Configuracion de Spark
conf = SparkConf()
conf.setAppName("TwitterCovid")

# Creamos el contexto
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")

# Creamos el streamingContext con un timepo de 5 segundos
ssc = StreamingContext(sc, 5)

# setting a checkpoint to allow RDD recovery
# Configuramos un "checkpoint" para permitir recuperar el RDD
ssc.checkpoint("../checkpoint_TwitterCovid")

# Leemos los datos desde localhost por el puerto 5556
dataStream = ssc.socketTextStream("localhost",5556)

# separamos el tweet por palabras usando split para los espacios
words = dataStream.flatMap(lambda line: line.split(' '))

  
# filter the words to get only hashtags, then map each hashtag to be a pair of (hashtag,1)
hashtags = words.map(lambda x: (x, 1)) 

# añadimos nuevos datos refresh
tags_totals = hashtags.updateStateByKey(aggregate_tags_count)

# Procesamiento de los RDD en cada intervalo de tiempo
tags_totals.foreachRDD(process_rdd)


ssc.start()
ssc.awaitTermination()