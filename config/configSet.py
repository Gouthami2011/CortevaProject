import os
import logging
from pyspark.sql import SparkSession
from pathlib import Path
import os
from dotenv import load_dotenv

log = logging.getLogger(__name__)

# Fetches all the environmental values for both spark and Flask API
def setEnvironement(test=None):
    path = Path(os.getcwd()).absolute()
    dotenv_path = os.path.join(path, "config/.env")
    
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    if test is None:

        DATA_DIR = os.path.join(path, "Data")

    else:

        DATA_DIR = os.path.join(os.path.join(path, "TestData"), "Data")

    os.environ['WEATHERDATA'] = os.path.join(DATA_DIR, "wx_data")
    os.environ['YIELDDATA'] = os.path.join(DATA_DIR, "yld_data")
    os.environ['SPARK_DB_DRIVER'] = os.path.join(path, "jar/postgresql-42.2.5.jar")

# Sets Spark Dataframe for running spark
def get_spark():
    spark = SparkSession.builder.config("spark.jars", os.environ.get('SPARK_DB_DRIVER')) \
	.master("local").appName("PySpark_Postgres_test").getOrCreate()

    return spark