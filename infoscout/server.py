from flask import Flask, render_template
from model import generate_retailer_data, generate_percent_sales_table, retailer_affinity, count_hhs, top_buying_brand
import pandas as pd
import matplotlib

matplotlib.use('TkAgg')

app=Flask(__name__)

@app.route("/")
def root():
    return "Hello Worldgs"

@app.route("/affinity")
def percent_sales_table():
    data = generate_retailer_data()
    df = generate_percent_sales_table(data)
    return render_template('template.html',tables=[df.to_html()], titles = ['na', 'Percent Sales'])

@app.route("/affinity2")
def total_sales_table():
    data = generate_retailer_data()
    df = pd.DataFrame(data)
    return render_template('template.html',tables=[df.to_html()], titles = ['na', 'Total Sales'])

@app.route("/affinity3")
def find_affinity():
    return retailer_affinity('Monster')

@app.route("/HHcount")
def HHcount():
    return str(count_hhs())

@app.route("/TopBuying")
def top_brand():
    return top_buying_brand()

if __name__ == '__main__':
    app.run(debug=True)
