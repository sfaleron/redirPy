import os
import glob

from zipfile import ZipFile

fd = open('.pending', 'rb')

zipf = ZipFile(fd.read() + '.zip', 'w')

fd.close()

os.remove('.pending')

for fn in glob.glob('input*'):
   zipf.write(fn)

for fn in glob.glob('output*'):
   zipf.write(fn)
   os.remove(fn)

zipf.close()
