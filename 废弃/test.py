import re
s ='''
<div class = 'jay' ><span id = '1'>郭麒麟</span></div>
'''
obj = re.compile(r"<div class = '.*?' ><span id = '\d+'>(?P<wahaha>.*?)</span></div>", re.S)
#obj = re.compile(r"<div class = '.*?' ><span id = '\d+'>.*?</span></div>", re.S)
re = obj.finditer(s)
for i in re:
    print(i.group('wahaha'))