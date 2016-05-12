# removes all output expected to differ between pythonic and system modes,
# so they may be compared.

import os

import re
r = re.compile('-?[0-9]+')

for fn in os.listdir('.'):
   fin  = open(fn, 'r')
   fout = open(fn+'-temp', 'w')

   for ln in fin:
      if 'child' in ln:
         continue
      if 'excess' in ln:
         ln = r.sub('-99', ln)
      if '_py.py' in ln:
         ln = ln.replace('_py.py', '_.py')
      if '_sys.py' in ln:
         ln = ln.replace('_sys.py', '_.py')

      fout.write(ln)

   fin.close()
   fout.close()

   os.rename(fn+'-temp', fn)
