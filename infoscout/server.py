from flask import Flask, request, render_template
from model import generate_retailer_data, generate_percent_sales_table, retailer_affinity, count_hhs, top_buying_brand
import pandas as pd
import matplotlib

matplotlib.use('TkAgg')

app=Flask(__name__)

@app.route("/", methods = [ 'GET' ])
def root():
    return render_template('template.html')

@app.route("/affinity", methods = [ 'POST' ])
def percent_sales_table():
    data = generate_retailer_data()
    df = generate_percent_sales_table(data)
    RA = None
    if len(request.form.get('brand')):
        RA = retailer_affinity(request.form.get('brand'))
    return render_template('template.html',table=df.to_html(), affinity=RA)
@app.route("/HHcount", methods = [ 'POST' ])
def HHcount():
    brand = None
    retailer = None
    start_date = None
    end_date = None
    if len(request.form.get('brand')):
        brand = request.form.get('brand')
    if len(request.form.get('retailer')):
        retailer = request.form.get('retailer')
    if len(request.form.get('start_date')):
        start_date = request.form.get('start_date')
    if len(request.form.get('end_date')):
        end_date = request.form.get('end_date')
    house_holds = count_hhs(brand, retailer, start_date, end_date)
    return render_template('template.html', results = house_holds)

@app.route("/TopBuying")
def top_brand():
    top_brand =  top_buying_brand()
    return render_template('template.html', top_brand = top_brand)

if __name__ == '__main__':
    app.run(debug=True)
