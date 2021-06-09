# Load repeaters JSON file
repeaters_json = open('repeaters.json').read()

# Apply change to repeaters HTML page
lines = open('repeaters.html').read().splitlines()
lines[164] = 'var treeData = '+str(repeaters_json)+';'
open('repeaters.html', 'w').write('\n'.join(lines))
