import urllib.request

# Fetch sheet as CSV
sheet_url = 'https://docs.google.com/spreadsheets/d/1W27KNa6yJzYA_b8HLSz4hxtWEZQtxUhGTXfQjlXgpzY/gviz/tq?tqx=out:csv&sheet={{Catalogue}}'
urllib.request.urlretrieve(sheet_url, 'catalogue.csv')
