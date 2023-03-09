import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, Request, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement=Base.classes.measurement
station=Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/(start date)<br/>"
        f"/api/v1.0/(start date)/(end date)"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
# Perform a query to retrieve the data and precipitation scores
    precipitation=session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= dt.datetime(2016,8,23))
    session.close()
    # Create a dictionary from the row data and append
    precip = []
    for date, prcp in precipitation:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip.append(precip_dict)
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
# Perform a query    
    stations=session.query(station.station).all()
    session.close()

    #Return a list from the data
    stations = [tuple(row) for row in stations]
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
# Perform a query    
    year=session.query(measurement.date, measurement.tobs).\
        filter(measurement.station=='USC00519281', measurement.date>=dt.datetime(2016,8,23)).all()
    session.close()

    # Create a dictionary from the row data and append
    observations = []
    for date, tobs in year:
        obs_dict = {}
        obs_dict["date"] = date
        obs_dict["tobs"] = tobs
        observations.append(obs_dict)
    return jsonify(observations)

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
# Perform a query    
    max_temp=session.query(func.max(measurement.tobs)).\
        filter(measurement.date>=start).all()

    min_temp=session.query(func.min(measurement.tobs)).\
        filter(measurement.date>=start).all()

    avg_temp=session.query(func.avg(measurement.tobs)).\
        filter(measurement.date>=start).all()
    session.close()

#create a dictionary from the data and output
    output={"max temp": max_temp[0][0], "min temp": min_temp[0][0], "avg temp": round(avg_temp[0][0],2)}
    return jsonify(output)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
# Perform a query    
    max_temp=session.query(func.max(measurement.tobs)).\
        filter(measurement.date<= end, measurement.date>=start).all()

    min_temp=session.query(func.min(measurement.tobs)).\
        filter(measurement.date<= end, measurement.date>=start).all()

    avg_temp=session.query(func.avg(measurement.tobs)).\
        filter(measurement.date<= end, measurement.date>=start).all()
    session.close()
#create a dictionary from the data and output
    output={"max temp": max_temp[0][0], "min temp": min_temp[0][0], "avg temp": round(avg_temp[0][0],2)}
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
