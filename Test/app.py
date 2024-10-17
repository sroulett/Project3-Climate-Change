from flask import Flask, jsonify, render_template
import pandas as pd
# Import the dependencies.
# import datetime as dt
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import sqlite3

#################################################
# Database Setup
#################################################
# engine = create_engine("sqlite:///../climate_change.db")
# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(autoload_with=engine)
# Data = Base.classes.temp_change

# # Create our session (link) from Python to the DB
# session = Session(engine)
#################################################
# Flask Setup
#################################################


app = Flask(__name__)

# Load your database
# data = pd.read_csv('your_data.csv')
# conn = sqlite3.connect('climate_change.db')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/temperature_data')
def temperature_data():
    # Process data to get average temperature per decade
    # This is just an example; you'll need to implement the logic
    conn = sqlite3.connect('climate_change.db')
    result_df = pd.read_sql("SELECT * FROM temp_change where dt >= '1860-01-01'", conn)
    result_df['dt'] = pd.to_datetime(result_df['dt'])
    result_df.set_index('dt', inplace = True)
    date_temp_df = result_df[['Country','AverageTemperature']].copy()
    date_temp_df['decade'] = (date_temp_df.index.year // 10) * 10
    average_temp_per_decade_df = date_temp_df.groupby(['Country', 'decade'])['AverageTemperature'].mean().reset_index()
    average_temp_per_decade_df.columns = ['Country','Decade', 'AverageTemperature']
    average_temp_per_decade_df = average_temp_per_decade_df.dropna()
    return jsonify(average_temp_per_decade_df.to_dict(orient='records'))

    

if __name__ == '__main__':
    app.run(debug=True)


    