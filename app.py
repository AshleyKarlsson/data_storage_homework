import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station 
Measurement = Base.classes.measurement

#########################################################################
# Flask Setup
app = Flask(__name__)

# List all routes that are available.
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start/end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary list of dates and precipitation"""
    # Query all precipitatioin
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    session.close()

    # Create dictionary of query results and print in JSON format
    all_precip = []
    for precip in results:
        precip_dict = {}
        precip_dict["Date"] = precip.date
        precip_dict["Precipitation"] = precip.prcp
        all_precip.append(precip_dict) 
    
    return jsonify(all_precip)

@app.route("/api/v1.0/stations")
def stations():
   
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of all station names"""
    # Query all stations
    results = session.query(Measurement.station).group_by(Measurement.station).all()
    session.close()
    
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature for past year"""
    # Query all temperatures
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
              group_by(Measurement.date).\
              filter(Measurement.date > 23-8-2016).\
              order_by(Measurement.station).all()
    session.close()

    # Create dictionary of query results and print in JSON format
    temp_data = []
    for tobs in results:
        tobs_dict = {}
        tobs_dict["Station"] = tobs.station
        tobs_dict["Date"] = tobs.date
        tobs_dict["Temperature"] = tobs.tobs
        temp_data.append(tobs_dict)
    
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of measurement data"""
    # Query all measurement data for start date (YYMMDD)
    start = start.replace(" ", "")
    results = session.query(func.avg(Measurement.tobs),func.min(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()    
    session.close()

    # Print measurement data in JSON format
    temperature_range= list(np.ravel(results))
    return jsonify(temperature_range)

@app.route("/api/v1.0/<start>/<end>")
def startandend(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of measurement data"""
    # Query all measurement data for date range (YYMMDD/YYMMDD)
    start = start.replace(" ", "")
    end = end.replace(" ", "")
    results = session.query(func.avg(Measurement.tobs),func.min(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    session.close()    
    
    # Print measurement data in JSON format
    temp_range= list(np.ravel(results))
    return jsonify(temp_range) 
    
if __name__ == '__main__':
    app.run(debug=True)