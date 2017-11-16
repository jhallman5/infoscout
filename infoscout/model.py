import requests
import pandas as pd
from datetime import datetime

def generate_retailer_data():
    """Returns the number of sales for each retailer per brand."""
    AWSjson = requests.get('https://s3.amazonaws.com/isc-isc/trips_gdrive.json').json()
    retailers = {item['retailer']: {} for item in AWSjson}
    for item in AWSjson:
        if(retailers[item['retailer']].get(item["brand"], None)):
            retailers[item['retailer']][item["brand"]] += int(item["qty"])
        else:
            retailers[item['retailer']][item["brand"]] = int(item["qty"])
    return retailers

def generate_percent_sales_table(retailerData):
    """Returns the sale percentages per brand for each retailer."""
    df = pd.DataFrame(retailerData)
    for column in df:
        new_df = df.agg(column).apply(lambda x: percentages(x, df[column]))
        df.update(new_df)
    return df

def percentages(item, retailer):
    """Generates percentage of item sales per retailer."""
    interFloat =  100 * item /float(retailer.sum())
    return round(interFloat, 2)

def generate_user_data(options):
    AWSjson = requests.get('https://s3.amazonaws.com/isc-isc/trips_gdrive.json').json()
    users = {item['userId'] for item in AWSjson if filter_user_data(item, options)}
    print(len(users))
    return users

def filter_user_data(item, options):
    if options.get('brand'):
        if item['brand'] != options['brand']:
            return False
    if options.get('retailer'):
        if item['retailer'] != options['retailer']:
            return False
    if options.get('start_date'):
        start_date = datetime.strptime(options['start_date'], '%m/%d/%Y')
        item['date'] = datetime.strptime(item['date'], '%m/%d/%Y')
        if item['date'] < start_date:
            return False
    if options.get('end_date'):
        end_date = datetime.strptime(options['end_date'], '%m/%d/%Y')
        item['date'] = datetime.strptime(item['date'], '%m/%d/%Y')
        if item['date'] > end_date:
            return False
    return True

# Function solutions
def retailer_affinity(focus_brand):
    """Returns the strongest retailer affinity relative to other brands."""
    data = generate_retailer_data()
    df = generate_percent_sales_table(data)
    return df.ix[focus_brand].idxmax(axis=1)

def count_hhs(brand=None, retailer=None, start_date=None, end_date=None):
    """A function that returns the number of households allowing for a dynamic optional set of inputs."""
    options = {
        'brand': brand,
        'retailer': retailer,
        'start_date': start_date,
        'end_date': end_date
        }
    data = generate_user_data(options)
    return None

def top_buying_brand():
    """Identify brand with top buying rate ($ spent / HH)."""
    return None
