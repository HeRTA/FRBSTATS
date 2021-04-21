import numpy as np
from astropy import units as  u
import astropy.coordinates as apycoords
from astropy.coordinates import SkyCoord
from shutil import copyfile
from csv import reader
import urllib.request
import matplotlib
import matplotlib.pyplot as plt

# Use TeX
plt.rcParams['text.usetex'] = True

# Adjust figsize
plt.rcParams["figure.figsize"] = (35,35)

# Load data
# Initiate empty parameter lists
l = []
b = []
dm = []

# Read FRBSTATS CSV catalogue
with open('../catalogue.csv', 'r') as read_obj:
	csv_reader = reader(read_obj)
	header = next(csv_reader)
	# Skip header
	if header != None:
		for row in csv_reader:
			l.append(row[6])
			b.append(row[7])
			dm.append(row[9])

# Pre-process data (pick out incompatible rows)
idx_mask = set()
for idx, val in enumerate(l):
	try:
		l[idx] = float(val)
	except ValueError:
		idx_mask.add(idx)

for idx, val in enumerate(b):
	try:
		b[idx] = float(val)
	except ValueError:
		idx_mask.add(idx)

for idx, val in enumerate(dm):
	try:
		dm[idx] = float(val)
	except ValueError:
		idx_mask.add(idx)

# Dump rows with missing data
for idx in sorted(idx_mask, reverse=True):
	del l[idx]
	del b[idx]
	del dm[idx]

# Convert l, b to RA, Dec.
ras = []
decs = []
for idx in range(len(l)):
	c = SkyCoord(l[idx], b[idx], frame='galactic', unit='deg')
	c = c.icrs
	ras.append(c.ra.hour)
	decs.append(c.dec.deg)

# Load HI survey
survey = np.loadtxt('map.txt')

# Flip array to match RA and Dec axes
#survey_corrected = survey
survey_corrected = np.flip(survey, 0)

# Plot map
plt.imshow(survey_corrected.T, extent=[-90,90,24,0], aspect=4, interpolation='gaussian')

# Plot properties
plt.title(r'$\mathrm{FRB \ } \delta \mathrm{-} \alpha \mathrm{ \ Distribution}$', fontsize=70, y=1.01)
plt.xlabel(r'$\mathrm{Declination \ [deg]}$', fontsize=50)
plt.ylabel(r'$\mathrm{Right \ Ascension \ [h]}$', fontsize=50)
plt.yticks(np.arange(0, 24.01, 2))
plt.xticks(fontsize=36)
plt.yticks(fontsize=36)

# Plot given source position
plt.scatter(decs, ras, c=dm, s=400, alpha=0.6, edgecolor='white', linewidth=2, cmap='plasma')

# Set colorbar
cbar = plt.colorbar(ticks=[300, 600, 900, 1200, 1500, 1800, 2100, 2400], orientation="horizontal", aspect=30, pad=0.08)
cbar.set_label(r'$\mathrm{Dispersion \ Measure \ }\Bigg[\mathrm{pc \ cm}^{-3}\Bigg]$', fontsize=52)
cbar.ax.tick_params(labelsize=42)

# Remove alpha colorbar component
cbar.set_alpha(1)
cbar.draw_all()

# Add survey citation
plt.text(40.5, -0.31, r'$\mathrm{LAB \ HI \ Survey \ (Kalberla \ et \ al., \ 2005)}$', fontsize=34, bbox={'facecolor': 'white', 'pad': 5})

# Save plot to file
plt.savefig('ra_dec.svg', bbox_inches='tight')
plt.savefig('ra_dec.pdf', bbox_inches='tight')
plt.savefig('ra_dec.png', bbox_inches='tight')