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
frequency = []
width = []

# Read FRBSTATS CSV catalogue
with open('../catalogue.csv', 'r') as read_obj:
	csv_reader = reader(read_obj)
	header = next(csv_reader)
	# Skip header
	if header != None:
		for row in csv_reader:
			frequency.append(row[8])
			width.append(row[11])

### Pre-process data
# Pick out incompatible rows
idx_mask = set()
for idx, val in enumerate(frequency):
        try:
                frequency[idx] = float(val)
        except ValueError:
                idx_mask.add(idx)

for idx, val in enumerate(width):
	try:
		width[idx] = float(val)
	except ValueError:
		idx_mask.add(idx)

# Dump rows with missing data
for idx in sorted(idx_mask, reverse=True):
	del frequency[idx]
	del width[idx]

### Initiate plot
# Apply grid
plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=1)

# Scatter plot
plt.scatter(frequency, width, c='cornflowerblue', s=500, alpha=0.8, edgecolor='royalblue', linewidth=2, zorder=10)

# Set axis labels & figure title
plt.xlabel(r'$\mathrm{Center \ Frequency \ [MHz]}$', fontsize=52)
plt.ylabel(r'$\mathrm{Burst \ Width \ [ms]}$', fontsize=52)
plt.title(r'$\mathrm{FRB \ Width-Frequency \ Distribution}$', fontsize=72, y=1.01)

# Set axis scaling
#plt.xscale('log')
plt.yscale('log')

# Set axis limits
plt.gca().set_xlim(left=0)

# Set tick size
plt.xticks(fontsize=42, y=-0.005)
plt.yticks(fontsize=42)

plt.tight_layout()

# Save data to a scalable format
plt.savefig('width_frequency.svg', format='svg')
plt.savefig('width_frequency.pdf')
plt.savefig('width_frequency.png')
