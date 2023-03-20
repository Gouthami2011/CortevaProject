import os
from config.configSet import get_spark, setEnvironement
import logging
from app.ETL.ETlProcess import creatTables, readFiles, transformWeatherData, writeToTable, dataAnalysisWeather, transformYieldData
from pyspark.sql.types import *

logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

#Let us Create an object 
log=logging.getLogger() 

#Now we are going to Set the threshold of logger to DEBUG 
log.setLevel(logging.DEBUG) 

# Creating Schema for the dataframe to read from txt file
weatherSchema = StructType() \
      .add("Date",IntegerType(),False) \
      .add("MaxTemp",StringType(),True) \
      .add("MinTemp",StringType(),True) \
      .add("Precipitation",StringType(),True) \

yeildSchema = StructType() \
      .add("Year",IntegerType(),False) \
      .add("Yield",StringType(),True)

# Peforms the complete ETL process for the project
def performETL(log):
    
    log.warning('This message will get logged on to a file')
    setEnvironement()
    spark = get_spark()
    log.info("Create tables if not exists...")
    
    # creatTables(spark, log)

    # Reads weather data table and loads it into dataframe
    weatherDF = readFiles(spark, log, os.environ.get('WEATHERDATA'), weatherSchema)

    # Reads Yield data table and loads it into dataframe
    yeildDF = readFiles(spark, log, os.environ.get('YIELDDATA'), yeildSchema)

    if not(weatherDF.rdd.isEmpty()):
        
        # Performs weather data preprocessing for loading it into table
        weatherDF = transformWeatherData(weatherDF, log)

        # Peforms transformation necessary for the creating new data analysis table into dataframe
        transformedWeatherDf = dataAnalysisWeather(weatherDF, log)

        #Writes weather dataframe into Weather table
        writeToTable(weatherDF, 'Weather', log)

        #Writes transformedWeatherDf dataframe into Weather_Analysis table
        writeToTable(transformedWeatherDf, 'Weather_Analysis', log)

    if not(yeildDF.rdd.isEmpty()):
        # Performs yield data preprocessing for loading it into table
        yeildDF = transformYieldData(yeildDF, log)


        #Writes yeildDF dataframe into yield table
        writeToTable(yeildDF, 'Yield', log)

    log.info("Analysis process complete!")

performETL(log)