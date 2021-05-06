import json
import os

# Load FRB repeater parents from JSON data
with open('../../repeaters.json') as f:
	channels = json.loads(f.read())

parents = []
for parent in range(len(channels[0]['children'])):
	parents.append(channels[0]['children'][parent]['name'])

# Plot for every parent
for repeater in parents:
	print(repeater)
	os.system('python3 plot_repeaters.py "' + repeater + '"')
