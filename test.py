# -*- coding: utf-8 -*-

import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#text = u'\u56de\u590d:@BeaJerk\uff1a\u67d0\u8bf4\u4eca\u5929\uff0c\u6539\u5929 '
text = u'回复:@BeaJerk：某说今天，改天 '
m = re.match(u'回复:?@([^:]+):(.*)\s+', text, re.DOTALL)
print m
if m:
	print m.group(1)
