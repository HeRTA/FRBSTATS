import sys
import json
from csv import reader
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np

### Set MPL plot parameters
# Selectable SVG text
plt.rcParams['svg.fonttype'] = 'none'

# Use TeX
plt.rcParams['text.usetex'] = True

# Set figsize
plt.rcParams["figure.figsize"] = (24,12)
plt.rcParams["figure.dpi"] = 300

# Set xtick size
plt.rcParams['xtick.major.size'] = 20
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['xtick.minor.size'] = 10
plt.rcParams['xtick.minor.width'] = 2

# Set ytick size
plt.rcParams['ytick.major.size'] = 20
plt.rcParams['ytick.major.width'] = 2
plt.rcParams['ytick.minor.size'] = 10
plt.rcParams['ytick.minor.width'] = 2

# Hide secondary spines
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

repeater = str(sys.argv[1])

### Load data
# Initiate empty parameter lists
with open('../../repeaters.json') as f:
    channels = json.loads(f.read())

parents = []
for parent in range(len(channels[0]['children'])):
        parents.append(channels[0]['children'][parent]['name'])

frb_index = parents.index(repeater)
children = []
for child in range(len(channels[0]['children'][frb_index]['children'])):
        children.append(channels[0]['children'][frb_index]['children'][child]['name'])

frb = [parents[frb_index]] + children

telescope = []
snr = []
mjd = []
ra = []
ra_error = []
dec = []
dec_error = []
dm = []
dm_error = []

# Read FRBSTATS CSV catalogue
with open('../../catalogue.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        # Skip header
        if header != None:
                for row in csv_reader:
                        if any(burst in row for burst in frb):
                                telescope.append(row[3])
                                snr.append(row[13])
                                ra.append(row[4])
                                ra_error.append(row[17])
                                dec.append(row[5])
                                dec_error.append(row[18])
                                dm.append(row[9])
                                dm_error.append(row[19])
                                mjd.append(row[2])

### Pre-process data
# Pick out incompatible rows
idx_mask = set()

for idx, val in enumerate(telescope):
        if str(val) != '-':
                telescope[idx] = str(val)
        else:
                idx_mask.add(idx)

for idx, val in enumerate(snr):
        try:
                snr[idx] = float(val)
        except ValueError:
                idx_mask.add(idx)

for idx, val in enumerate(mjd):
        try:
                mjd[idx] = float(val)
        except:
                idx_mask.add(idx)

# Dump rows with missing data
for idx in sorted(idx_mask, reverse=True):
        del frb[idx]
        del telescope[idx]
        del snr[idx]
        del mjd[idx]
        del dm[idx]
        del ra[idx]
        del dec[idx]

### Initiate table plot
column_labels = ['FRB','MJD','Telescope','RA','RA Error','Dec.','Dec. Error','DM','DM Error','S:N']
frb_np = np.array(frb)
mjd_np = np.array(mjd)
telescope_np = np.array(telescope)
ra_np = np.array(ra)
ra_error_np = np.array(ra_error)
dec_np = np.array(dec)
dec_error_np = np.array(dec_error)
dm_np = np.array(dm)
dm_error_np = np.array(dm_error)
snr_np = np.array(snr)

data = np.column_stack([frb_np, mjd_np, telescope_np, ra_np, ra_error_np, dec_np, dec_error_np, dm_np, dm_error_np, snr_np])
plt.axis('tight')
plt.axis('off')
plt.table(cellText=data,colLabels=column_labels,cellLoc="center",loc="center",colColours=["lightskyblue"]*7,colWidths=[1/22,1/26,1/22,1/24,1/24,1/34,1/34])

plt.tight_layout()

# Save data to a scalable format
plt.savefig(frb[0].lower().replace(' ', '_')+'_table.pdf')
