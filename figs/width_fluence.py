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
plt.rcParams["figure.figsize"] = (26,20)
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
dm = []
fluence = []
width = []

# Read FRBSTATS CSV catalogue
with open('../catalogue.csv', 'r') as read_obj:
	csv_reader = reader(read_obj)
	header = next(csv_reader)
	# Skip header
	if header != None:
		for row in csv_reader:
			dm.append(row[9])
			fluence.append(row[12])
			width.append(row[11])

### Pre-process data
# Pick out incompatible rows
idx_mask = set()
for idx, val in enumerate(dm):
        try:
                dm[idx] = float(val)
        except ValueError:
                idx_mask.add(idx)

for idx, val in enumerate(fluence):
	try:
		fluence[idx] = float(val)
	except ValueError:
		idx_mask.add(idx)

for idx, val in enumerate(width):
        try:
                width[idx] = float(val)
        except ValueError:
                idx_mask.add(idx)

# Dump rows with missing data
for idx in sorted(idx_mask, reverse=True):
	del dm[idx]
	del fluence[idx]
	del width[idx]

### Initiate plot
# Apply grid
plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=1)

# Scatter plot
plt.scatter(fluence, width, c=dm, s=500, alpha=0.7, edgecolor='black', linewidth=2, cmap='plasma', zorder=10)

# Set colorbar
cbar = plt.colorbar()
cbar.set_label(r'$\mathrm{Dispersion \ Measure \ }\Bigg[\mathrm{pc \ cm}^{-3}\Bigg]$', fontsize=52)
cbar.ax.tick_params(labelsize=42)

# Remove alpha colorbar component
cbar.set_alpha(1)
cbar.draw_all()

# Set axis labels & figure title
plt.xlabel(r'$\mathrm{Burst \ Fluence \ [Jy \ ms]}$', fontsize=52)
plt.ylabel(r'$\mathrm{Burst \ Width \ [ms]}$', fontsize=52)
plt.title(r'$\mathrm{FRB \ Width-Fluence \ Distribution}$', fontsize=72, y=1.01)

# Set log-log scaling
plt.xscale('log')
plt.yscale('log')

# Set ylim
#plt.xlim(10**-1,10**4)
#plt.ylim(10**-2,10**3)

# Set tick size
plt.xticks(fontsize=42, y=-0.005)
plt.yticks(fontsize=42)

plt.tight_layout()

# Save data to a scalable format
plt.savefig('width_fluence.svg', format='svg')
plt.savefig('width_fluence.pdf')
plt.savefig('width_fluence.png')
