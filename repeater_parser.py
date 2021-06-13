# Load repeaters JSON file
repeaters_json = open('~/public_html/frbstats/repeaters.json').read()

# Apply change to repeaters HTML page
lines = open('~/public_html/frbstatsrepeaters.html').read().splitlines()
lines[164] = 'var treeData = '+str(repeaters_json)+';'

open('~/public_html/frbstatsrepeaters.html', 'w').write('\n'.join(lines))
