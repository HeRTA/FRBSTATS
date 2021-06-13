# Load repeaters JSON file
repeaters_json = open('/home/herta-experiment/public_html/frbstats/repeaters.json').read()

# Apply change to repeaters HTML page
lines = open('/home/herta-experiment/public_html/frbstats/repeaters.html').read().splitlines()
lines[164] = 'var treeData = '+str(repeaters_json)+';'

open('/home/herta-experiment/public_html/frbstats/repeaters.html', 'w').write('\n'.join(lines))
