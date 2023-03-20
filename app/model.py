import psycopg2
import os

def weatherAnalysisFetch(dateValue, StationID, page):
    data = []
    per_page=int(os.environ.get('MAX_PAGE')) # Sets max records it can fetch from table
    
    #Calculating offset for fetching data based on pages
    offsetPage = (int(page) - 1) * per_page

    # Connects to postgres database using the env variable
    connection = psycopg2.connect(database=os.environ.get('dbDatabase'), user=os.environ.get('dbUserName'), password=os.environ.get('dbPassword'), host=os.environ.get('dbHost'), port=os.environ.get('dbPort'))
    cursor = connection.cursor()

    # Checks whether the year for the stats are integer and is off 4 chanracters and checking stationID is not null
    if (dateValue and len(dateValue) == 4 and dateValue.isnumeric()) and StationID:
        cursor.execute('''select "StationID","Year","AvgMaxTemp","AvgMinTemp","TtlAccPrecipitation" from Weather_Analysis where "StationID"='{StationID}' AND "Year"='{year}' ORDER BY "StationID" DESC LIMIT {limit} OFFSET {offset} ;'''.format(StationID=StationID, year=int(dateValue), limit = per_page, offset = offsetPage))
    # Checks whether the year for the stats are integer and is off 4 chanracters
    elif (dateValue and len(dateValue) == 4 and dateValue.isnumeric()):
        cursor.execute('''select "StationID","Year","AvgMaxTemp","AvgMinTemp","TtlAccPrecipitation" from Weather_Analysis where "Year"='{year}' ORDER BY "StationID" DESC LIMIT {limit} OFFSET {offset} ;'''.format(year=int(dateValue), limit = per_page, offset = offsetPage))
    # Checks stationID is not null
    elif StationID:
        cursor.execute('''select "StationID","Year","AvgMaxTemp","AvgMinTemp","TtlAccPrecipitation" from Weather_Analysis where "StationID"='{StationID}' ORDER BY "StationID" DESC LIMIT {limit} OFFSET {offset} ;'''.format(StationID=StationID, limit = per_page, offset = offsetPage))
    # Default fetch
    else:
        cursor.execute('''select "StationID","Year","AvgMaxTemp","AvgMinTemp","TtlAccPrecipitation" from Weather_Analysis ORDER BY "StationID" DESC LIMIT {limit} OFFSET {offset} ;'''.format(limit = per_page, offset = offsetPage))
    result = cursor.fetchall()

    if (result is tuple):
      user = {}
      user["StationID"] = result[0]
      user["Year"] = result[1]
      user["AvgMaxTemp"] = result[2]
      user["AvgMinTemp"] = result[3]
      user["TtlAccPrecipitation"] = result[4]
      data.append(user)
    else :
      for i in result:
        user = {}
        user["StationID"] = i[0]
        user["Year"] = i[1]
        user["AvgMaxTemp"] = i[2]
        user["AvgMinTemp"] = i[3]
        user["TtlAccPrecipitation"] = i[4]
        data.append(user)
    
    connection.commit()
    connection.close()

    final = {
       "count":len(data),
       "Data":data,
       "Page":page
    }

    return final	


def weatherFetch(yearVal,monthVal,dateVal,StationID, page):
    data = []
    per_page=int(os.environ.get('MAX_PAGE'))  # Sets max records it can fetch from table

    #Calculating offset for fetching data based on pages
    offsetPage = (int(page) - 1) * per_page

    # Connects to postgres database using the env variable
    connection = psycopg2.connect(database=os.environ.get('dbDatabase'), user=os.environ.get('dbUserName'), password=os.environ.get('dbPassword'), host=os.environ.get('dbHost'), port=os.environ.get('dbPort'))
    cursor = connection.cursor()

    # Checks whether the date for the stats are integer and is off 8 chanracters and checking stationID is not null
    if ((yearVal and dateVal and monthVal) and (len(dateVal) + len(monthVal) + len(yearVal)) == 8 and dateVal.isnumeric() and monthVal.isnumeric() and yearVal.isnumeric()) and StationID:
        cursor.execute('''select "StationID","Year","Month","Date","MaxTemp","MinTemp","Precipitation" from weather where "StationID"='{StationID}' AND "Year"='{year}' AND "Month"='{month}' AND "Date"='{dateVal}' ORDER BY "StationID" DESC LIMIT {limit} OFFSET {offset} ;'''.format(StationID=StationID, year=yearVal, month=monthVal,  dateVal=dateVal, limit = per_page, offset = offsetPage))
    # Checks whether the date for the stats are integer and is off 8 chanracters
    elif ((yearVal and dateVal and monthVal) and (len(dateVal) + len(monthVal) + len(yearVal)) == 8 and dateVal.isnumeric() and monthVal.isnumeric() and yearVal.isnumeric()) :
        cursor.execute('''select "StationID","Year","Month","Date","MaxTemp","MinTemp","Precipitation" from weather where "Year"='{year}' AND "Month"='{month}' AND "Date"='{dateVal}' ORDER BY "StationID" DESC LIMIT {limit} OFFSET {offset} ;'''.format(year=yearVal, month=monthVal,  dateVal=dateVal, limit = per_page, offset = offsetPage))
    # Checks stationID is not null
    elif StationID:
        cursor.execute('''select "StationID","Year","Month","Date","MaxTemp","MinTemp","Precipitation" from weather where "StationID"='{StationID}' ORDER BY "StationID" DESC LIMIT {limit} OFFSET {offset} ;'''.format(StationID=StationID, limit = per_page, offset = offsetPage))
    # Default fetch
    else:
        cursor.execute('''select "StationID","Year","Month","Date","MaxTemp","MinTemp","Precipitation" from weather ORDER BY "StationID" DESC LIMIT {limit} OFFSET {offset} ;'''.format(limit = per_page, offset = offsetPage))
    result = cursor.fetchall()

    if (result is tuple):
      user = {}
      user["StationID"] = result[0]
      user["Year"] = result[1]
      user["Month"] = result[2]
      user["Date"] = result[3]
      user["MaxTemp"] = result[4]
      user["MinTemp"] = result[5]
      user["Precipitation"] = result[6]
      data.append(user)
    else :
      for i in result:
        user = {}
        user["StationID"] = i[0]
        user["Year"] = i[1]
        user["Month"] = i[2]
        user["Date"] = i[3]
        user["MaxTemp"] = i[4]
        user["MinTemp"] = i[5]
        user["Precipitation"] = i[6]
        data.append(user)
    
    connection.commit()
    connection.close()

    final = {
       "count":len(data),
       "Data":data,
       "Page":page
    }
    return final	