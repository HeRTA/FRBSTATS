import pandas as pd
import csv

# Load TNS data
f = pd.read_csv('tns_search.csv', dtype=str)

# Strip unnecessary columns
keep_col = ['Name', 'RA', 'DEC', 'DM', 'Discovery Date (UT)', 'Discovery Mag/Flux']
new_f = f[keep_col]

# Rearrange column positions
new_f = new_f[['Name', 'Discovery Date (UT)', 'RA', 'DEC', 'DM', 'Discovery Mag/Flux']]

# Rename columns
new_f.columns = ['frb', 'utc', 'ra', 'dec', 'dm', 'flux']

# Strip whitespace from FRB names
new_f["frb"] = new_f["frb"].str.split().apply("".join)

# Insert columns
new_f.insert(2, 'mjd', '0')
new_f.insert(3, 'telescope', '0')
new_f.insert(6, 'l', '0')
new_f.insert(7, 'b', '0')
new_f.insert(8, 'frequency', '0')
new_f.insert(11, 'width', '0')
new_f.insert(12, 'fluence', '0')
new_f.insert(13, 'status', 'N')

# Write changes to file
new_f.to_csv('catalogue.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
