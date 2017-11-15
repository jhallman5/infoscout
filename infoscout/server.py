from flask import Flask, render_template
from model import generate_brand_data, generate_retailer_data
import requests
import json
import pandas as pd
import matplotlib
from matplotlib.pyplot import pie, axis, show
import numpy as np

matplotlib.use('TkAgg')


app=Flask(__name__)

@app.route("/")
def hello():
    results = requests.get('https://s3.amazonaws.com/isc-isc/trips_gdrive.json')
    return "Hello Worldgs"

@app.route("/affinity")
def goodbye():
    # generate_brand_data()
    return "goodbye"

@app.route("/affinity2")
def goodbye2():
    data = generate_retailer_data()
    df = pd.DataFrame(data)
    df_og = pd.DataFrame(data)
    for column in df:
        new_df = df.agg(column).apply(lambda x: percentages(x, df[column]))
        df.update(new_df)
    return render_template('template.html',tables=[df_og.to_html(), df.to_html()], titles = ['na', 'Raw Sales', 'Percent Sales'])


def percentages(item, retailer):
     interFloat =  100 * item /float(retailer.sum())
     return round(interFloat, 2)


if __name__ == '__main__':
    app.run(debug=True)
