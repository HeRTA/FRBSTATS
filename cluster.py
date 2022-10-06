eps = 87

import json
import random
import numpy as np
from csv import reader
from sklearn.cluster import *
from astropy import units as u
from astropy.coordinates import Angle
from matplotlib.ticker import EngFormatter

### Load data
# Initiate empty parameter lists

frb = []
ra = []
ra_error = []
dec = []
dec_error = []
dm = []
dm_error = []

# Read FRBSTATS CSV catalogue
with open('/home/herta-experiment/public_html/frbstats/catalogue.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        # Skip header
        if header != None:
                for row in csv_reader:
                        frb.append(row[0])
                        ra.append(row[4])
                        ra_error.append(row[17])
                        dec.append(row[5])
                        dec_error.append(row[18])
                        dm.append(row[9])
                        dm_error.append(row[19])

### Pre-process data
# Pick out incompatible rows
idx_mask = set()
for idx, val in enumerate(dm):
        try:
                dm[idx] = float(val)
        except ValueError:
                idx_mask.add(idx)

# Dump rows with missing data
for idx in sorted(idx_mask, reverse=True):
        del frb[idx]
        del dm[idx]
        del ra[idx]
        del dec[idx]

# Convert coordinates to rad and turn '-' (N/A) to +/- 0 uncertainty
for i in range(len(ra)):
        ra[i] = Angle(str(ra[i])+' hr').rad
for i in range(len(ra_error)):
        if ra_error[i] == '-':
                ra_error[i] = 0
        ra_error[i] = Angle(str(ra_error[i])+ ' arcmin').rad

for i in range(len(dec)):
        dec[i] = Angle(str(dec[i])+' deg').rad
for i in range(len(dec_error)):
        if dec_error[i] == '-':
                dec_error[i] = 0
        dec_error[i] = Angle(str(dec_error[i])+ ' arcmin').rad

for i in range(len(dm_error)):
        if dm_error[i] == '-':
                dm_error[i] = 0

X = np.array([[ra[i], ra_error[i], dec[i], dec_error[i], dm[i], dm_error[i]] for i in range(len(frb))])

def dist(frb1, frb2):
        # Point A
        ra1 = frb1[0]
        dec1 = frb1[2]
        dm1 = frb1[4]

        # Errors
        ra_error1 = frb1[1]
        dec_error1 = frb1[3]
        dm_error1 = frb1[5]

        # Point B
        ra2 = frb2[0]
        dec2 = frb2[2]
        dm2 = frb2[2]

        # Errors
        ra_error2 = frb2[1]
        dec_error2 = frb2[3]
        dm_error2 = frb2[5]

        # Coordinate A
        x1 = dm1*np.cos(dec1)*np.sin(ra1)
        y1 = dm1*np.cos(dec1)*np.cos(ra1)
        z1 = dm1*np.sin(dec1)

        # Partial derivatives
        dx_dRA1 = dm1*np.cos(dec1)*np.cos(ra1)
        dy_dRA1 = -dm1*np.cos(dec1)*np.sin(ra1)
        dz_dRA1 = 0

        dx_dDec1 = -dm1*np.sin(ra1)*np.sin(dec1)
        dy_dDec1 = -dm1*np.cos(ra1)*np.sin(dec1)
        dz_dDec1 = dm1*np.cos(dec1)

        dx_dDM1 = np.cos(dec1)*np.sin(ra1)
        dy_dDM1 = np.cos(dec1)*np.cos(ra1)
        dz_dDM1 = np.sin(dec1)

        # Uncertainties
        Dx1 = np.sqrt((dx_dRA1**2) * (ra_error1**2) + (dx_dDec1**2) * (dec_error1)**2 + (dx_dDM1**2) * (dm_error1)**2)
        Dy1 = np.sqrt((dy_dRA1**2) * (ra_error1**2) + (dy_dDec1**2) * (dec_error1)**2 + (dy_dDM1**2) * (dm_error1)**2)
        Dz1 = np.sqrt((dz_dRA1**2) * (ra_error1**2) + (dz_dDec1**2) * (dec_error1)**2 + (dz_dDM1**2) * (dm_error1)**2)

        # Coordinate B
        x2 = dm2*np.cos(dec2)*np.sin(ra2)
        y2 = dm2*np.cos(dec2)*np.cos(ra2)
        z2 = dm2*np.sin(dec2)

        # Partial derivatives
        dx_dRA2 = dm2*np.cos(dec2)*np.cos(ra2)
        dy_dRA2 = -dm2*np.cos(dec2)*np.sin(ra2)
        dz_dRA2 = 0

        dx_dDec2 = -dm2*np.sin(ra2)*np.sin(dec2)
        dy_dDec2 = -dm2*np.cos(ra2)*np.sin(dec2)
        dz_dDec2 = dm2*np.cos(dec2)

        dx_dDM2 = np.cos(dec2)*np.sin(ra2)
        dy_dDM2 = np.cos(dec2)*np.cos(ra2)
        dz_dDM2 = np.sin(dec2)

        # Uncertainties
        Dx2 = np.sqrt((dx_dRA2**2) * (ra_error2**2) + (dx_dDec2**2) * (dec_error2)**2 + (dx_dDM2**2) * (dm_error2)**2)
        Dy2 = np.sqrt((dy_dRA2**2) * (ra_error2**2) + (dy_dDec2**2) * (dec_error2)**2 + (dy_dDM2**2) * (dm_error2)**2)
        Dz2 = np.sqrt((dz_dRA2**2) * (ra_error2**2) + (dz_dDec2**2) * (dec_error2)**2 + (dz_dDM2**2) * (dm_error2)**2)

        # Compute Euclidean distance
        d = np.sqrt(((x1-x2)**2)+((y1-y2)**2)+((z1-z2)**2))

        # Compute error
        dd_dx1 = (x1-x2)/np.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
        dd_dy1 = (y1-y2)/np.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
        dd_dz1 = (z1-z2)/np.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)

        dd_dx2 = -(x1-x2)/np.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
        dd_dy2 = -(y1-y2)/np.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
        dd_dz2 = -(z1-z2)/np.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)

        Dd = np.sqrt(
                ((dd_dx1)**2) * Dx1**2 +
                ((dd_dy1)**2) * Dy1**2 +
                ((dd_dz1)**2) * Dz1**2 +

                ((dd_dx2)**2) * Dx2**2 +
                ((dd_dy2)**2) * Dy2**2 +
                ((dd_dz2)**2) * Dz2**2
        )

        return d #/Dd

# Cluster FRB repeaters
db = DBSCAN(eps=eps, min_samples=2, metric=dist, n_jobs=-1).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_
# Dump clusters to JSON file
cluster_json = ''
for i in range(np.max(labels)+1):
        print('-------- '+str(i)+' --------')
        repeater_cluster = []
        for j in np.where(labels == i)[0]:
                print(frb[j]+':'+str(ra[j])+','+str(dec[j])+','+str(dm[j]))
                repeater_cluster.append(frb[j])
        parent = True
        for k in repeater_cluster:
                if parent:
                        parent_frb = k
                        cluster_json += '{"name":"'+k+'","parent":"Repeaters","children":['
                        parent = False
                else:
                        cluster_json += '{"name":"'+k+'","parent":"'+parent_frb+'"},'
        cluster_json = cluster_json[:-1] + ']},'
cluster_json = cluster_json[:-1]

repeaters = '[{"name":"Repeaters","parent":"null","children":['+cluster_json+']}]'

with open('repeaters.json', 'w') as f:
        json.dump(json.loads(repeaters), f, indent=3, sort_keys=False)

# Load repeaters JSON file
repeaters_json = open('/home/herta-experiment/public_html/frbstats/repeaters.json').read()

# Apply change to repeaters HTML page
lines = open('/home/herta-experiment/public_html/frbstats/repeaters.html').read().splitlines()
lines[164] = 'var treeData = '+str(repeaters_json)+';'

open('/home/herta-experiment/public_html/frbstats/repeaters.html', 'w').write('\n'.join(lines))

### Plot repeater clusters
import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

### Set MPL plot parameters
# Selectable SVG text
plt.rcParams['svg.fonttype'] = 'none'

# Use TeX
plt.rcParams['text.usetex'] = True

# Set figsize
plt.rcParams['figure.figsize'] = (24,12)
plt.rcParams['figure.dpi'] = 300

fig = plt.figure(figsize=(24, 12))

### Repeaters
ax = fig.add_subplot(1, 2, 2, projection='3d')

ax.set_xlim3d(0,360)
ax.set_ylim3d(-90,90)

ax.xaxis.set_major_formatter(EngFormatter(unit=u'°'))
ax.yaxis.set_major_formatter(EngFormatter(unit=u'°'))

ax.set_xlabel(r'$\mathrm{Galactic \ Longitude\ } (l)$', fontsize=24, labelpad=18)
ax.set_ylabel(r'$\mathrm{Galactic \ Latitude\ } (b)$', fontsize=24, labelpad=18)
ax.set_zlabel(r'$\mathrm{Dispersion \ Measure \ }\bigg[\mathrm{pc \ cm}^{-3}\bigg]$', fontsize=24, labelpad=23)

ax.tick_params(axis='both', which='major', labelsize=22)
ax.tick_params(axis='both', which='minor', labelsize=22)
ax.tick_params(axis='z', which='major', pad=12)
ax.tick_params(axis='z', which='minor', pad=12)

ax.set_title(r'$\mathrm{Repeater \ Clusters}$', fontdict={'fontsize':36})

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

# Use black as noise points (one-offs)
unique_labels = set(labels)
colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]

for k, col in zip(unique_labels, colors):
        if k == -1:
                # Noise color (R,G,B,A)
                col = [0, 0, 0, 0.3]
        else:
                # Semi-transparent repeater color (A)
                col = list(col)
                col[3] = 0.3
                col = tuple(col)

        class_member_mask = labels == k

        xy = X[class_member_mask & core_samples_mask]
        ax.plot(
                xy[:, 0],
                xy[:, 1],
                xy[:, 2],
                'o',
                markerfacecolor=tuple(col),
                markeredgecolor='k',
                markersize=10,
                markeredgewidth=0.9,
        )

### One-offs
ax = fig.add_subplot(1, 2, 1, projection='3d')

ax.set_xlim3d(0,360)
ax.set_ylim3d(-90,90)

ax.xaxis.set_major_formatter(EngFormatter(unit=u'°'))
ax.yaxis.set_major_formatter(EngFormatter(unit=u'°'))

ax.set_xlabel(r'$\mathrm{Galactic \ Longitude\ } (l)$', fontsize=24, labelpad=18)
ax.set_ylabel(r'$\mathrm{Galactic \ Latitude\ } (b)$', fontsize=24, labelpad=18)
ax.set_zlabel(r'$\mathrm{Dispersion \ Measure \ }\bigg[\mathrm{pc \ cm}^{-3}\bigg]$', fontsize=24, labelpad=25)

ax.tick_params(axis='both', which='major', labelsize=22)
ax.tick_params(axis='both', which='minor', labelsize=22)
ax.tick_params(axis='z', which='major', pad=12)
ax.tick_params(axis='z', which='minor', pad=12)

ax.set_title(r'$\mathrm{One}$-$\mathrm{Off \ Events}$', fontdict={'fontsize':36})

for k, col in zip(unique_labels, colors):
        if k == -1:
                # Noise color (R,G,B,A)
                col = [0, 0, 0, 0.3]
        else:
                # Semi-transparent repeater color (A)
                col = list(col)
                col[3] = 0.3
                col = tuple(col)
        xy = X[class_member_mask & ~core_samples_mask]
        ax.plot(
                xy[:, 0],
                xy[:, 1],
                xy[:, 2],
                'o',
                markerfacecolor=tuple(col),
                markeredgecolor='k',
                markersize=10,
                markeredgewidth=0.9,
        )

#plt.title('$\mathrm{Estimated \ number \ of \ repeaters: %d}$' % n_clusters_)
plt.tight_layout(pad=7)

plt.savefig('/home/herta-experiment/public_html/frbstats/figs/repeaters/repeaters.svg', format='svg')
plt.savefig('/home/herta-experiment/public_html/frbstats/figs/repeaters/repeaters.pdf')
plt.savefig('/home/herta-experiment/public_html/frbstats/figs/repeaters/repeaters.png')
