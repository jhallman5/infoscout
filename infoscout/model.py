import requests
import pandas as pd
from datetime import datetime

def generate_retailer_data():
    """Returns the number of sales for each retailer per brand."""
    AWSjson = requests.get('https://s3.amazonaws.com/isc-isc/trips_gdrive.json').json()
    retailers = {item['retailer']: {} for item in AWSjson}
    for item in AWSjson:
        if retailers[item['retailer']].get(item["brand"]):
            retailers[item['retailer']][item["brand"]] += int(item["qty"])
        else:
            retailers[item['retailer']][item["brand"]] = int(item["qty"])
    return retailers

def generate_percent_sales_table(retailerData):
    """Returns a sales percentages dataframe per brand and retailer."""
    df = pd.DataFrame(retailerData)
    for column in df:
        new_df = df.agg(column).apply(lambda x: percent_convertion(x, df[column]))
        df.update(new_df)
    return df

def percent_convertion(item, retailer):
    """Generates percentage of item sales per retailer."""
    percentSales =  100 * item /int(retailer.sum())
    return round(percentSales, 2)

def number_of_users(options, AWSjson):
    """Returns number of users, applies filters if necessary."""
    if not AWSjson:
        AWSjson = requests.get('https://s3.amazonaws.com/isc-isc/trips_gdrive.json').json()
    users = {item['userId'] for item in AWSjson if filter_user_data(item, options)}
    return len(users)

def filter_user_data(item, options):
    """Helper Function, Applies filters to set comprehension."""
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

def count_hhs(brand=None, retailer=None, start_date=None, end_date=None, AWSjson=None):
    """A function that returns the number of households allowing for a dynamic optional set of inputs."""
    options = {
        'brand': brand,
        'retailer': retailer,
        'start_date': start_date,
        'end_date': end_date
        }
    return number_of_users(options, AWSjson)

def top_buying_brand():
    """Identify brand with top buying rate ($ spent / HH)."""
    AWSjson = requests.get('https://s3.amazonaws.com/isc-isc/trips_gdrive.json').json()
    brands = { item['brand'] for item in AWSjson }
    top_brand = (0,0)
    for brand in brands:
        buying_rate = gross_income(brand, AWSjson) / count_hhs(brand, None, None, None, AWSjson )
        if buying_rate > top_brand[1]:
            top_brand = (brand, buying_rate)
    return top_brand[0]

def gross_income(brand, AWSjson):
    """Returns the gross income of a brand."""
    result = 0
    for item in AWSjson:
        if item['brand'] == brand:
            result += int(item['amount'][1:])
    return result
