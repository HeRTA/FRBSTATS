import urllib.request
import os

# Fetch sheet as CSV
sheet_url = 'https://docs.google.com/spreadsheets/d/1W27KNa6yJzYA_b8HLSz4hxtWEZQtxUhGTXfQjlXgpzY/gviz/tq?tqx=out:csv&sheet={{Catalogue}}'
urllib.request.urlretrieve(sheet_url, 'catalogue_tmp.csv')

# Replace blank instances with "-"
with open('catalogue_tmp.csv', 'rt') as fin:
	with open('catalogue.csv', 'wt') as fout:
		for line in fin:
			fout.write(line.replace('""', '"-"'))

# Delete temporary catalogue file
os.remove('catalogue_tmp.csv')
