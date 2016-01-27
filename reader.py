import db
import time

n_users = 1620997
n_blogs = 156365006

from progressbar import *
widgets = ['Progress: ', Percentage(), ' ', Bar(marker = '>'), ' ', ETA()]

con = db.connect()
if con == None:
	exit()

cur = con.cursor()

id_hist = {}
pbar = ProgressBar(widgets = widgets, maxval = n_blogs).start()
cur.execute('select user_id from microblogs')

count = 0
for tmp in cur:
	user_id = tmp[0]
	print user_id
	break
	if id_hist.has_key(user_id):
		id_hist[user_id] += 1
	else:
		id_hist[user_id] = 1

	pbar.update(count)
pbar.finish()

fobj = open('res.txt', 'w')
fobj.write('\n'.join(['%d %d'%(k, v) for k, v in id_hist.items()]))
fobj.close()

cur.close()
con.close()