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

### Load data
# Initiate empty parameter lists
dm = []
flux = []

# Read FRBSTATS CSV catalogue
with open('../catalogue.csv', 'r') as read_obj:
	csv_reader = reader(read_obj)
	header = next(csv_reader)
	# Skip header
	if header != None:
		for row in csv_reader:
			dm.append(row[9])
			flux.append(row[10])

### Pre-process data
# Pick out incompatible rows
idx_mask = set()
for idx, val in enumerate(dm):
        try:
                dm[idx] = float(val)
        except ValueError:
                idx_mask.add(idx)

for idx, val in enumerate(flux):
	try:
		flux[idx] = float(val)
	except ValueError:
		idx_mask.add(idx)

# Dump rows with missing data
for idx in sorted(idx_mask, reverse=True):
	del dm[idx]
	del flux[idx]

### Initiate plot
# Apply grid
plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=1)

# Scatter plot
plt.scatter(flux, dm, c='cornflowerblue', s=500, alpha=0.8, edgecolor='royalblue', linewidth=2, zorder=10)

# Set axis labels & figure title
plt.xlabel(r'$\mathrm{Peak \ Flux \ Density \ [Jy]}$', fontsize=52)
plt.ylabel(r'$\mathrm{Dispersion \ Measure \ }\Bigg[\mathrm{pc \ cm}^{-3}\Bigg]$', fontsize=52)
plt.title(r'$\mathrm{FRB \ DM-Flux \ Distribution}$', fontsize=72, y=1.01)

# Set log-log scaling
plt.xscale('log')
#plt.yscale('log')

# Set axis limits
plt.gca().set_ylim(bottom=0)

# Set tick size
plt.xticks(fontsize=42, y=-0.005)
plt.yticks(fontsize=42)

# Remove top and right border
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.gca().xaxis.set_tick_params(top='off',which='both')
plt.gca().yaxis.set_tick_params(right='off',which='both')

plt.tight_layout()

# Save data to a scalable format
plt.savefig('dm_flux.svg', format='svg')
plt.savefig('dm_flux.pdf')
plt.savefig('dm_flux.png')
