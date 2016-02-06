
import cPickle
import matplotlib.pyplot as plt

from const import PKL_REPORT

valid_hist, comm_hist, emo_tf, emo_df = cPickle.load(open('data/report.pkl', 'r'))

total_valid = sum([k * v for k, v in valid_hist.items()])

report = ''
report += 'number of users: %d\n'%(sum(valid_hist.values()))
report += 'total_valid: %d\n'%(total_valid)
report += 'max_valid: %d\n'%(max(valid_hist.keys()))
report += 'min_valid: %d\n'%(min(valid_hist.keys()))
report += 'types of emotion: %d\n'%(len(emo_tf))
report += 'max_tf: %d\n'%(max(emo_tf.values()))
report += 'min_tf: %d\n'%(min(emo_tf.values()))
report += 'max_df: %d\n'%(max(emo_df.values()))
report += 'min_df: %d\n'%(min(emo_df.values()))

print report

print '\n########### TF ###############'
emo_tf = sorted(emo_tf.items(), key = lambda k: -k[1])
for i, item in enumerate(emo_tf):
	emo, count = item
	print '%d. %s (%d / %d)'%(i + 1, emo, count, emo_df[emo])

plt.figure()
valid_items = sorted(valid_hist.items(), key = lambda k:k[0])
x = [k for k, v in valid_items]
y = [v for k, v in valid_items]
plt.plot(x, y)
plt.savefig('output/valid.png')

plt.figure()
comm_items = sorted(comm_hist.items(), key = lambda k:k[0])
x = [k for k, v in comm_items]
y = [v for k, v in comm_items]
plt.plot(x, y)
plt.savefig('output/comm.png') 
