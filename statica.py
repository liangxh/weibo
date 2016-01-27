import matplotlib.pyplot as plt

fobj = open('res.txt', 'r')
content = fobj.read()
fobj.close()

idhist = {}
for item in content.split('\n'):
	params = item.split(' ')
	idhist[int(params[0])] = int(params[1])

print len(idhist.keys())
phist = {}
for v in idhist.values():
	if phist.has_key(v):
		phist[v] += 1
	else:
		phist[v] = 1

plt.figure()
plt.plot(phist.keys(), phist.values())
plt.savefig('phist.png')

phist = sorted(phist.items(), key = lambda k:-k[1])
vt = phist[0][0]

print phist[0]
print phist[1]

ids = []
for k, v in idhist.items():
	if v == vt:
		ids.append(str(k))

print len(ids)
fobj = open('ids.txt', 'w')
fobj.write('\n'.join(ids))
fobj.close()
