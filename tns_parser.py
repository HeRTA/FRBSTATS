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
new_f['frb'] = new_f['frb'].str.split().apply(''.join)

# Insert columns
new_f.insert(2, 'mjd', '?')
new_f.insert(3, 'telescope', '?')
new_f.insert(4, 'sefd', '?')
new_f.insert(7, 'l', '?')
new_f.insert(8, 'b', '?')
new_f.insert(9, 'frequency', '?')
new_f.insert(12, 'width', '?')
new_f.insert(13, 'fluence', '?')
new_f.insert(14, 'snr', '?')
new_f.insert(15, 'status', 'N')

# Write changes to file
new_f.to_csv('catalogue.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
