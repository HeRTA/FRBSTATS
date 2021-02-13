import csv
import json

# Catalogue headers
fieldnames = ('frb', 'utc', 'mjd', 'telescope', 'ra', 'dec', 'l', 'b', 'frequency', 'dm', 'flux', 'width', 'fluence', 'status')

with open('catalogue.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames)
    header = reader.fieldnames

    with open('catalogue.json', 'w') as jsonfile:
        # Prepend brace
        jsonfile.write('[\n')

        first = True
        for row in reader:
            if first:
                # Skip header
                first = False
                continue
            else:
                json.dump(row, jsonfile)
                jsonfile.write('\n')

        # Append brace
        jsonfile.write(']')

# Read json file
with open('catalogue.json', 'r') as f:
    filedata = f.read()

# Append comma separators
filedata = filedata.replace('}\n{', '},\n{').replace('}{', '},{')

# Output parsed json
with open('catalogue.json', 'w') as file:
    file.write(filedata)
