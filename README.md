# Corteva Data Analysis
Task: Perform analysis on the weather and yield data given in https://github.com/corteva/code-challenge-template and given some requirement for performing ETL operation

Tools/Software Package Used:
Docker, postgre, PySpark, Flask

Docker was utilised for easy deploying process, Postgres was used for its OLTP and OTAP properties and PySpark is used for inproving the performance of the ETL operation. 

Major Steps in Acheving given task
1. Perform ETL operation:
2. Load transformed data into table
    Entire ETL operation was performed in main.py code. 

3. Create API end points for accessing the loaded data into table
    Flask API REST points are
    1. http://0.0.0.0:5000/api/weather?year=<year>&month=<month>&date=<date>&StationID=<StationID>
    2. http://0.0.0.0:5000/api/weather/<PageNumber>?year=<year>&month=<month>&date=<date>&StationID=<StationID>
    3. http://0.0.0.0:5000/api/weather/Stats?year=<year>&StationID=<StationID>
    4. http://0.0.0.0:5000/api/weather/Stats/<PageNumber>?year=<year>&StationID=<StationID>

# How to run the project     
docker compose up

# Deployment:

1. AWS S3 - Store the file which needs to be processed on ETL
2. AWS EMR - EMR can be used for running data ingestion and data transformation spark code
3. AWS RDS - Host the database for writing the transformed data into table. This table will be read by Flask API. 
4. AWS EC2 - EC2 can be used for creating VM where Flask API can he hosted there.

