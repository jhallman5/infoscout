import requests
import pandas as pd

# def generate_brand_data():
#     """Returns the number of sales for each brand at each retailer."""
#     AWSjson = requests.get('https://s3.amazonaws.com/isc-isc/trips_gdrive.json').json()
#     brands = {item['brand']: {} for item in AWSjson}
#     for item in AWSjson:
#         if(brands[item['brand']].get(item["retailer"], None)):
#             brands[item['brand']][item["retailer"]] += int(item["qty"])
#         else:
#             brands[item['brand']][item["retailer"]] = int(item["qty"])
#     return brands

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

def retailer_affinity(focus_brand):
    """Returns the strongest retailer affinity relative to other brands."""
    data = generate_retailer_data()
    df = generate_percent_sales_table(data)
    return df.ix[focus_brand].idxmax(axis=1)
