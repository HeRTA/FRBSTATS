import requests
import os

# Fetch sheet as CSV
sheet_url = 'https://docs.google.com/spreadsheets/d/1W27KNa6yJzYA_b8HLSz4hxtWEZQtxUhGTXfQjlXgpzY/gviz/tq?tqx=out:csv&sheet={{Catalogue}}'
requests.get(sheet_url)

# Rename file to catalogue.csv
os.rename('data.csv', 'catalogue.csv')
