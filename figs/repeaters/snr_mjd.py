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

### Load data
# Initiate empty parameter lists
frb = ['FRB 20190907A', 'FRB 20190915A', 'FRB 20190925A', 'FRB 20200307A']
telescope = []
snr = []
mjd = []

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

### Initiate plot
# Apply grid
plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=1)

# Define telescope colors
telescope_clr = {
	'Arecibo': 'orange',
	'ASKAP': 'green',
	'CHIME': 'red',
	'DSA-10': 'violet',
	'Effelsberg': 'aquamarine',
	'FAST': 'cyan',
	'GBT': 'purple',
	'GMRT': 'yellow',
	'INAF SRT': 'olive',
	'Parkes': 'royalblue',
	'Pushchino LPA': 'lightcoral',
	'Stockert': 'brown',
	'UTMOST': 'chocolate'
}

# Scatter plot
plt.scatter(mjd, snr, c=[telescope_clr[i] for i in telescope], s=600, linewidth=2, zorder=10)
plt.plot(mjd, snr, c='black', linestyle='--', linewidth=2, zorder=5)

for tel, clr in telescope_clr.items():
	if tel in telescope:
		plt.plot([],[], marker='o', markersize=25, linestyle='', label=r'$\mathrm{'+tel.replace(' ', r'\ ')+r'}$', c=clr)

# Set axis labels & figure title
plt.xlabel(r'$\mathrm{Modified \ Julian \ Date}$', fontsize=52, labelpad=9)
plt.ylabel(r'$\mathrm{Detection \ S/N}$', fontsize=52, labelpad=12)
plt.title(r'$\mathrm{'+frb[0].replace(' ', r' \ ')+' \ }-\mathrm{ \ Repeater \ Time \ Series}$', fontsize=72, y=1.03)

# Enable legend
plt.legend(numpoints=1, fontsize=34)

# Set log-log scaling
#plt.xscale('log')
#plt.yscale('log')

# Set axis limits
#plt.xlim(0,7000)
#plt.ylim(0,3000)

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
plt.savefig('snr_mjd.svg', format='svg')
plt.savefig('snr_mjd.pdf')
plt.savefig('snr_mjd.png')
