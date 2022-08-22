import csv
import json

data_ads = 'datasets/ads.csv'
json_ads = "ads.json"
data_cat = "datasets/categories.csv"
json_cat = 'categories.json'
data_user = 'datasets/users.csv'
json_user = "users.json"
data_location = 'datasets/location.csv'
json_location = 'locations.json'


def convert_file(csv_file, model_name, json_file):
    result = []
    with open(csv_file, encoding='utf-8') as file:
        for row in csv.DictReader(file):
            if model_name == 'ads.category':
                to_add = {"model": model_name, "pk": int(row['id'])}
                del row['id']
            elif model_name == 'ads.user':
                to_add = {"model": model_name, "pk": int(row['id'])}
                del row['id']
            elif model_name == 'ads.location':
                to_add = {"model": model_name, "pk": int(row['id'])}
                del row['id']
            else:
                to_add = {"model": model_name, "pk": int(row['Id'])}
                del row['Id']
            if 'is_published' in row:
                if row['is_published'] == 'TRUE':
                    row['is_published'] = True
                else:
                    row['is_published'] = False
            if 'price' in row:
                row['price'] = int(row['price'])
            to_add['fields'] = row

            result.append(to_add)
    with open(json_file, 'w', encoding='utf-8') as jfile:
        jfile.write(json.dumps(result, ensure_ascii=False))


convert_file(data_ads, "ads.ad", json_ads)
convert_file(data_cat, "ads.category", json_cat)
convert_file(data_user, "ads.user", json_user)
convert_file(data_location, "ads.location", json_location)
