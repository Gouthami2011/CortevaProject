# Previous imports remain...
from flask import Flask, request
import unittest
import os
from main import *
from app import create_app
from app.model import weatherAnalysisFetch, weatherFetch
from config.configSet import setEnvironement
from flask_swagger_ui import get_swaggerui_blueprint

def create_app():

    app = Flask(__name__)
    ### swagger specific ###
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "CortevaApp"
        }
    )

    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    ### end swagger specific ###

    @app.route("/api/weather/Stat", methods=['get'])
    def weatherAnalysis():  
        dateValue  = request.args.get('year', None)
        StationID  = request.args.get('StationID', None)
        return weatherAnalysisFetch(dateValue, StationID, 1)
        

    @app.route("/api/weather/Stat/<page>", methods=['get'])
    def weatherAnalysisPage(page):  
        dateValue  = request.args.get('year', None)
        StationID  = request.args.get('StationID', None)
        return weatherAnalysisFetch(dateValue, StationID, int(page))

    @app.route("/api/weather", methods=['get'])
    def weather():  
        year  = request.args.get('year', None)
        month  = request.args.get('month', None)
        date  = request.args.get('date', None)
        StationID  = request.args.get('StationID', None)
        return weatherFetch(year,month,date,StationID, 1)
    
    @app.route("/api/weather/<page>", methods=['get'])
    def weatherPage(page):  
        year  = request.args.get('year', None)
        month  = request.args.get('month', None)
        date  = request.args.get('date', None)
        StationID  = request.args.get('StationID', None)
        return weatherFetch(year,month,date, StationID, int(page))  

    return app

setEnvironement()
app = create_app()
app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT'))