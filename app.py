# Previous imports remain...
from flask import Flask, request
import os
from app.model import weatherAnalysisFetch, weatherFetch
from config.configSet import setEnvironement

def create_app():
  app = Flask(__name__)

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

if __name__ == '__main__':
    setEnvironement()
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT'))
