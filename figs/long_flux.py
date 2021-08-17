from csv import reader
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

### Set MPL plot parameters
# Selectable SVG text
plt.rcParams['svg.fonttype'] = 'none'

# Use TeX
plt.rcParams['text.usetex'] = True

# Set figsize
plt.rcParams["figure.figsize"] = (24,20)
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

### Load data
# Initiate empty parameter lists
long = []
flux = []

# Read FRBSTATS CSV catalogue
with open('../catalogue.csv', 'r') as read_obj:
	csv_reader = reader(read_obj)
	header = next(csv_reader)
	# Skip header
	if header != None:
		for row in csv_reader:
			long.append(row[6])
			flux.append(row[10])

### Pre-process data
# Pick out incompatible rows
idx_mask = set()
for idx, val in enumerate(long):
        try:
                long[idx] = float(val)
        except ValueError:
                idx_mask.add(idx)

for idx, val in enumerate(flux):
	try:
		flux[idx] = float(val)
	except ValueError:
		idx_mask.add(idx)

# Dump rows with missing data
for idx in sorted(idx_mask, reverse=True):
	del long[idx]
	del flux[idx]

### Initiate plot
# Apply grid
plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=1)

# Scatter plot
plt.scatter(flux, long, c='cornflowerblue', s=500, alpha=0.8, edgecolor='royalblue', linewidth=2, zorder=10)

# Set axis labels & figure title
plt.xlabel(r'$\mathrm{Peak \ Flux \ Density \ [Jy]}$', fontsize=52)
plt.ylabel(r'$\mathrm{Gal. \ Longitude \ [deg]}$', fontsize=52)
plt.title(r'$\mathrm{FRB \ Gal. \ Longitude-Flux \ Distribution}$', fontsize=72, y=1.01)

# Set log-log scaling
plt.xscale('log')
#plt.yscale('log')

# Set axis limits
#plt.xlim(0,3000)
#plt.ylim(10**-2,10**3)

# Set tick size
plt.xticks(fontsize=42, y=-0.005)
plt.yticks(fontsize=42)

plt.tight_layout()

# Save data to a scalable format
plt.savefig('long_flux.svg', format='svg')
plt.savefig('long_flux.pdf')
plt.savefig('long_flux.png')
