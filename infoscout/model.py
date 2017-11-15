import requests

def generate_brand_data():
    """Returns the number of sales for each brand at each retailer."""
    AWSjson = requests.get('https://s3.amazonaws.com/isc-isc/trips_gdrive.json').json()
    brands = {item['brand']: {} for item in AWSjson}
    for item in AWSjson:
        if(brands[item['brand']].get(item["retailer"], None)):
            brands[item['brand']][item["retailer"]] += int(item["qty"])
        else:
            brands[item['brand']][item["retailer"]] = int(item["qty"])
    print(brands)
    return brands

def generate_retailer_data():
    """Returns the number of sales for each retailer per brand."""
    AWSjson = requests.get('https://s3.amazonaws.com/isc-isc/trips_gdrive.json').json()
    retailers = {item['retailer']: {} for item in AWSjson}
    for item in AWSjson:
        if(retailers[item['retailer']].get(item["brand"], None)):
            retailers[item['retailer']][item["brand"]] += int(item["qty"])
        else:
            retailers[item['retailer']][item["brand"]] = int(item["qty"])
    print(retailers['Walmart'])
    return retailers

# def generate_percent_per_retailer(retailerData):
#     """Returns the sale percentages per brand for each retailer."""
#     for retailer in retailerData:
#         for brand in retailer:
#             print(brand)
#     # totalSales = {item['retailer'] : {} for item in retailerData}
#     return 1
#

# def retailer_affinity(focus_brand):
# """Returns the strongest retailer affinity relative to other brands."""
