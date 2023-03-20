#!/usr/bin/env bash
#Runs Spark ETL. Read data from Data folder and perform ETL to transform and save into different tables
python main.py

#App for API for the data in the tables
python app.py