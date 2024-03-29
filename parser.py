import csv
import json

# Catalogue headers
fieldnames = ('frb', 'utc', 'mjd', 'telescope', 'ra', 'dec', 'l', 'b', 'frequency', 'dm', 'flux', 'width', 'fluence', 'snr', 'ref', 'redshift', 'redshift_measured', 'ra_error', 'dec_error', 'dm_error')

# Load CSV catalogue
with open('catalogue.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames)
    header = reader.fieldnames

    # Write to JSON
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

# Replace blanks (empty cells) with 'x'
filedata = filedata.replace('""', '"x"')

# Output parsed json
with open('catalogue.json', 'w') as file:
    file.write(filedata)
