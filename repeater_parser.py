import numpy as np
from sklearn.cluster import *
from csv import reader
import json

### Load data
# Initiate empty parameter lists

frb = []
dm = []
long = []
lat = []

# Read FRBSTATS CSV catalogue
with open('/home/herta-experiment/public_html/frbstats/catalogue.csv', 'r') as read_obj:
	csv_reader = reader(read_obj)
	header = next(csv_reader)
	# Skip header
	if header != None:
		for row in csv_reader:
			frb.append(row[0])
			dm.append(row[9])
			lat.append(row[7])
			long.append(row[6])

### Pre-process data
# Pick out incompatible rows
idx_mask = set()
for idx, val in enumerate(dm):
	try:
		dm[idx] = float(val)
	except ValueError:
		idx_mask.add(idx)

for idx, val in enumerate(long):
	try:
		long[idx] = float(val)
	except ValueError:
		idx_mask.add(idx)

for idx, val in enumerate(lat):
	try:
		lat[idx] = float(val)
	except ValueError:
		idx_mask.add(idx)

# Dump rows with missing data
for idx in sorted(idx_mask, reverse=True):
	del frb[idx]
	del dm[idx]
	del long[idx]
	del lat[idx]

X = np.array([[long[i], lat[i], dm[i]] for i in range(len(frb))])

def dist(frb1, frb2):
	# Point A
	l1 = np.deg2rad(frb1[0])
	b1 = np.deg2rad(frb1[1])
	dm1 = frb1[2]

	# Point B
	l2 = np.deg2rad(frb2[0])
	b2 = np.deg2rad(frb2[1])
	dm2 = frb2[2]

	# Coordinate A
	x1 = dm1*np.cos(b1)*np.sin(l1)
	y1 = dm1*np.cos(b1)*np.cos(l1)
	z1 = dm1*np.sin(b1)

	# Coordinate B
	x2 = dm2*np.cos(b2)*np.sin(l2)
	y2 = dm2*np.cos(b2)*np.cos(l2)
	z2 = dm2*np.sin(b2)

	# Compuute Euclidean distance
	return np.sqrt(((x1-x2)**2)+((y1-y2)**2)+((z1-z2)**2))

# Cluster FRB repeaters
db = DBSCAN(eps=15, min_samples=2, metric=dist, n_jobs=-1).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Dump clusters to JSON file
cluster_json = ''
for i in range(np.max(labels)+1):
	#print('-------- '+str(i)+' --------')
	repeater_cluster = []
	for j in np.where(labels == i)[0]:
		#print(frb[j]+':'+str(long[j])+','+str(lat[j])+','+str(dm[j]))
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

with open('/home/herta-experiment/public_html/frbstats/repeaters.json', 'w') as f:
	json.dump(json.loads(repeaters), f, indent=3, sort_keys=False)

"""
### Plot repeater clusters
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection='3d')

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

# Use black as noise points (one-offs)
unique_labels = set(labels)
colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]

for k, col in zip(unique_labels, colors):
    if k == -1:
        # Noise color (R,G,B,A)
        col = [0, 0, 0, 0.2]

    class_member_mask = labels == k

	xy = X[class_member_mask & core_samples_mask]
	ax.plot(
		xy[:, 0],
		xy[:, 1],
		xy[:, 2],
		"o",
		markerfacecolor=tuple(col),
		markeredgecolor="k",
		markersize=6,
	)

	xy = X[class_member_mask & ~core_samples_mask]
	ax.plot(
		xy[:, 0],
		xy[:, 1],
		xy[:, 2],
		"o",
		markerfacecolor=tuple(col),
		markeredgecolor="k",
		markersize=6,
	)
	plt.title("Estimated number of clusters: %d" % n_clusters_)
	plt.show()
"""

# Load repeaters JSON file
repeaters_json = open('/home/herta-experiment/public_html/frbstats/repeaters.json').read()

# Apply change to repeaters HTML page
lines = open('/home/herta-experiment/public_html/frbstats/repeaters.html').read().splitlines()
lines[164] = 'var treeData = '+str(repeaters_json)+';'

open('/home/herta-experiment/public_html/frbstats/repeaters.html', 'w').write('\n'.join(lines))
