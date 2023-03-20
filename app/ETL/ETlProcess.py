import pandas as pd
from pyspark.sql import functions as fn
from pyspark.sql.types import *
import os
from pyspark.sql.functions import regexp_replace, col
from pyspark.sql.functions import sum as _sum


def creatTables(spark, log):

    log.info("Creating Weather Table...")

    spark.sql('''CREATE TABLE IF NOT EXISTS Weather(
					StationID VARCHAR(100) NOT NULL,
                    Year INTEGER  NOT NULL,
                    Month INTEGER  NOT NULL,
                    Date INTEGER  NOT NULL,
					MaxTemp INTEGER,
					MinTemp INTEGER,
                    Precipitation INTEGER);''')

    log.info("Table successfully create...")
    log.info("Creating Yield Table...")

    spark.sql('''CREATE TABLE IF NOT EXISTS Yield(
                        YEAR INTEGER,
                        Yield INTEGER);''')
    
    log.info("Table successfully create...")
    log.info("Creating Weather_Analysis Table...")

    spark.sql('''CREATE TABLE IF NOT EXISTS Weather_Analysis(
                        StationID VARCHAR(100) NOT NULL,
                        Year INTEGER  NOT NULL,
                        AvgMaxTemp INTEGER,
                        AvgMinTemp INTEGER,
                        TtlAccPrecipitation INTEGER);''')
    
    log.info("Table successfully create...")

def readFiles(spark, log, path, schema):

    log.info(f"Reading of files for {path}")

    df = spark.read.options(delimiter="\t").csv(path, schema).withColumn("StationID", fn.input_file_name())

    log.info(f"Reading of files completed and Read {df.count}")

    return df
    

def transformWeatherData(df, log):

    log.info(f"Transformation for the Weather Data started and Count of rec in dataframe is {df.count}")

    # Fethching file name by delimiting
    df = df.withColumn('StationID', fn.split(df['StationID'], '.txt').getItem(0)) 
    df = df.withColumn('StationID', fn.split(df['StationID'], '/')) 
    df = df.withColumn("StationID", col("StationID").getItem(fn.size(col("StationID"))-1)) 
    
    # Dropping duplicates based on col Date and Station ID as these are primary Keys
    df = df.dropDuplicates(["Date","StationID"])
    df = df.withColumn("Year", fn.col("Date")[0:4])
    df = df.withColumn("Month", fn.col("Date")[5:2])
    df = df.withColumn("Date", fn.col("Date")[7:2])

    df.na.drop(subset=["Date","StationID"])

    df.select(regexp_replace(col("MaxTemp"), " ", ""))
    df.select(regexp_replace(col("MinTemp"), " ", ""))
    df.select(regexp_replace(col("Precipitation"), " ", ""))
    
    df = df.withColumn(
            "MaxTemp",
            fn.when(df.MaxTemp == "-9999", None).otherwise(
                fn.col("MaxTemp").cast(IntegerType())
            )
        )
    df = df.withColumn(
            "MinTemp",
            fn.when(df.MinTemp == "-9999", None).otherwise(
                fn.col("MinTemp").cast(IntegerType())
            )
        )
    df = df.withColumn(
            "Precipitation",
            fn.when(df.Precipitation == "-9999", None).otherwise(
                fn.col("Precipitation").cast(IntegerType())
            )
        )

    log.info(f"Transformation for the Weather Data Completed and Count of rec in dataframe is {df.count}")

    return df

def transformYieldData(df, log):

    log.info(f"Transformation for the Yield Data started and Count of rec in dataframe is {df.count}")
    
    df.na.drop(subset=["Year"])
    df = df.dropDuplicates(["Year"])

    df.select(regexp_replace(col("Yield"), " ", ""))

    df = df.drop(df.StationID)

    df = df.withColumn(
            "Yield",
            fn.when(df.Yield == "-9999", None).otherwise(
                fn.col("Yield").cast(IntegerType())
            ),
        )

    log.info(f"Transformation for the Yield Data Completed and Count of rec in dataframe is {df.count}")

    return df

def writeToTable(df, tableName, log):

    if (df.rdd.isEmpty()):
        log.info(f"Emplty Dataframe {df}")
    else:    
        df.write.format("jdbc").options(
            url=os.environ.get('URL'),
            driver="org.postgresql.Driver",
            dbtable=tableName,
            user=os.environ.get('dbUserName'),
            password=os.environ.get('dbPassword')
        ).mode("overwrite").save()

        log.info(f"Write dataframe to {tableName}  is complete")

def dataAnalysisWeather(df, log):
    if (df.rdd.isEmpty()):
        log.info(f"Emplty Dataframe {df}")
        return None
    else:   
        log.info(f"Transformation for the Weather_Analysis Table started and Count of rec in dataframe are {df.count}")

        df = df.withColumn('MaxTemp', df['MaxTemp'].cast(IntegerType()))
        df = df.withColumn('MinTemp', df['MinTemp'].cast(IntegerType()))
        df = df.withColumn('Precipitation', df['Precipitation'].cast(IntegerType()))

        #Calculating separately for each fields for accurate results
        maxTempDf = df.select("Year", "StationID", "MaxTemp").na.drop(how="any")
        minTempDf = df.select("Year", "StationID", "MinTemp").na.drop(how="any")
        precipitationDf = df.select("Year", "StationID", "Precipitation").na.drop(how="any")

        group_cols = ["Year", "StationID"]

        maxTempDf = maxTempDf.groupBy(group_cols).agg(_sum("MaxTemp").alias("AvgMaxTemp"))

        minTempDf = minTempDf.groupBy(group_cols).agg(_sum("MinTemp").alias("AvgMinTemp"))

        precipitationDf = precipitationDf.groupBy(group_cols).agg(_sum("Precipitation").alias("TtlAccPrecipitation"))

        dataAnalysisWeatherDf = maxTempDf.join(minTempDf, ["Year", "StationID"], "outer").distinct()

        dataAnalysisWeatherDf = dataAnalysisWeatherDf.join(precipitationDf, ["Year", "StationID"], "outer").distinct()

        count = dataAnalysisWeatherDf.count()

        log.info(f"No of records to be loaded into Weather_Analysis table are {count}")
        
        return dataAnalysisWeatherDf.select("Year", "StationID", "AvgMaxTemp", "AvgMinTemp", "TtlAccPrecipitation")
