import numpy as np
from csv import reader
from astropy import units as  u
import astropy.coordinates as apycoords
from astropy.coordinates import SkyCoord
from mw_plot import MWSkyMap
import urllib.request
from matplotlib import pyplot as plt
from shutil import copyfile

# Use TeX
plt.rcParams['text.usetex'] = True

# Set fontsize
plt.rcParams['font.size'] = 38

# Obtain data
urllib.request.urlretrieve('https://raw.githubusercontent.com/HeRTA/FRBSTATS/main/catalogue.csv', 'catalogue.csv')

# Load data
# Initiate empty parameter lists
l = []
b = []
dm = []

# Read FRBSTATS CSV catalogue
with open('catalogue.csv', 'r') as read_obj:
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

# Set projection & properties
plot_instance = MWSkyMap(projection='aitoff', grayscale=False, figsize=(20, 12.5))

# alpha value for the milkyway image
plot_instance.imalpha = 1.

# set up plot title
plot_instance.title = r'$\mathrm{FRB \ } l \mathrm{-} b \mathrm{ \ Distribution}$'+'\n'
plot_instance.fontsize = 48
#plot_instance.s = 115
#plot_instance.c = dm
#plot_instance.cmap = 'plasma'
#print(l)
#print(b)

#l = [10, 20]
#b = [-30, 40]
ras = []
decs = []
for idx in range(len(l)):
	c = SkyCoord(l[idx], b[idx], frame='galactic', unit='deg')
	c = c.icrs
	ras.append(c.ra.deg)
	decs.append(c.dec.deg)
ras = ras * u.degree
decs = decs * u.degree

plot_instance.scatter(ras, decs, c=dm, s=150, alpha=0.6, edgecolor='white', linewidth=0.85, cmap='plasma')

# Add colorbar
img = plt.imshow(np.array([[min(dm), max(dm)]]), cmap='plasma', aspect = 0.5)
img.set_visible(False)

cbar = plt.colorbar(ticks=list(np.arange(0, max(dm), 300)), orientation="horizontal", fraction=0.06, pad=0.08)
cbar.set_label(r'$\mathrm{Dispersion \ Measure \ }\Bigg[\mathrm{pc \ cm}^{-3}\Bigg]$')#, fontsize=38)
cbar.ax.tick_params(labelsize=32)

# Save image to file
#plt.tight_layout()

plot_instance.savefig(file='long_lat.svg')
plot_instance.savefig(file='long_lat.pdf')
plot_instance.savefig(file='long_lat.png')

# Clone files for flipped axes
copyfile('long_lat.svg', 'lat_long.svg')
copyfile('long_lat.pdf', 'lat_long.pdf')
copyfile('long_lat.png', 'lat_long.png')

# Show the figure
#plot_instance.show()
