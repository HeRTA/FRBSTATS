import csv

# Delete columns
with open('tns_search.csv', 'rb') as source:
    rdr = csv.reader(source)
    with open('tns_search_OUT.csv', 'wb') as result:
        wtr = csv.writer(result)
        for r in rdr:
            wtr.writerow((r[1], r[2], r[3], r[6], r[7], r[11]))
