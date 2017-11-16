from flask import Flask, render_template
from model import generate_retailer_data, generate_percent_sales_table, retailer_affinity, count_hhs, generate_user_data, filter_user_data
import requests
import pandas as pd
import matplotlib

matplotlib.use('TkAgg')

app=Flask(__name__)

@app.route("/")
def hello():
    results = requests.get('https://s3.amazonaws.com/isc-isc/trips_gdrive.json')
    return "Hello Worldgs"

@app.route("/affinity")
def goodbye():
    data = generate_retailer_data()
    df = generate_percent_sales_table(data)
    return render_template('template.html',tables=[df.to_html()], titles = ['na', 'Percent Sales'])

@app.route("/affinity2")
def goodbye2():
    data = generate_retailer_data()
    df = pd.DataFrame(data)
    return render_template('template.html',tables=[df.to_html()], titles = ['na', 'Total Sales'])

@app.route("/affinity3")
def find_affinity():
    return retailer_affinity('Monster')

@app.route("/HHcount")
def HHcount():
    count_hhs()
    return "Hello Thur"

if __name__ == '__main__':
    app.run(debug=True)
