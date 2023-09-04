# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    return (
        f"Available routes: <br>"
        f"api/v1.0/precipitation <br>"
        f"api/v1.0/stations <br>"
        f"api/v1.0/tobs <br>"
        f"api/v1.0/<start><br>"
        f"api/v1.0/<start>/<end><br>"
    )"


@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    previous_year = dt.date(2010,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
                            filter(Measurement.date >= previous_year).all()
    
    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    session.close()
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)


    stations = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    
    station_list = []
    for x in stations:
        station_dict = {}
        station_dict["station"] = x[0]
        station_dict["name"] = x[1]
        station_list.append(station_dict)

    session.close()
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    previous_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    last_year_obs_results = session.query(Measurement.date, Measurement.tobs).\
                                    filter(Measurement.date >= previous_year,\
                                    Measurement.station == most_active_station_id).all()
    
    tobs_list = []
    for x in last_year_obs_results:
        tobs_dict = {}
        tobs_dict["date"] = x[0]
        tobs_dict["tobs"] = x[1]
        tobs_list.append(tobs_dict)
    
    session.close()
    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def start():

    session = Session(engine)
    previous_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),\
                            func.avg(Measurement.tobs).filter(Measurement.date >= previous_year).all())

    aggregation_list = []
    for x in results:
        agg_dict = {}
        agg_dict["Min"] = x[0]
        agg_dict["Max"] = x[1]
        agg_dict["Avg"] = x[2]
        aggregation_list.append(agg_dict)

    session.close()
    return jsonify(aggregation_list)


@app.route("/api/v1.0/<start>")
def start_end():

    session = Session(engine)

    previous_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    today = dt.date(2017,8,23)

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),\
                            func.avg(Measurement.tobs).filter(Measurement.date >= previous_year).\
                            filter(Measurement.tobs) <= today).all()
    
    aggregation_list = []
    for x in results:
        agg_dict = {}
        agg_dict["Min"] = x[0]
        agg_dict["Max"] = x[1]
        agg_dict["Avg"] = x[2]
        aggregation_list.append(agg_dict)

    session.close()
    return jsonify(aggregation_list)


if __name__ == '__main__':
    app.run(debug=True)




