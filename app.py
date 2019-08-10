import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

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
        f"/api/v1.0/all_measurements"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary list of dates and precipitation"""
    # Query all precipitatioin
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Convert list of tuples into normal list
    all_precip = list(np.ravel(results))
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
    results = session.query(Measurement.date, Measurement.tobs).all()
    session.close()

    # Convert list of tuples into normal list
    all_temps = list(np.ravel(results))
    return jsonify(all_temps)

@app.route("/api/v1.0/start")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of measurement data"""
    # Query all measurement data
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).all()  
    session.close()

    all_measurements = list(np.ravel(results))
    return jsonify(all_measurements)

if __name__ == '__main__':
    app.run(debug=True)