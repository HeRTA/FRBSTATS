repeaters_json = open('repeaters.json').read()
lines = open('repeaters.html').read().splitlines()
lines[162] = 'var treeData = '+str(repeaters_json)+';'
open('repeaters.html', 'w').write('\n'.join(lines))