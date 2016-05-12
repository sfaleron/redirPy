
import os
import sys

import os.path as osp

from time import strftime, localtime, time

if sys.platform == 'win32':
   from ctypes import windll, byref, c_uint
   handle_count   = c_uint()
   process_handle = windll.kernel32.GetCurrentProcess()

def count_open_files():
   # cygwin not tested
   if   sys.platform in ('win32', 'cygwin'):
      # GetProcessHandleCount returns zero on failure; call GetLastError
      # for the juicy details. The Win32 API docs are rather unhelpful
      # with respect to what errors are possible, but there doesn't
      # appear to be anything that might reasonably fail in this case,
      # although anything can happen during runtime in Python!
      return handle_count.value if windll.kernel32.GetProcessHandleCount(process_handle, byref(handle_count)) else -1

   elif sys.platform == 'linux2':
      return len(os.listdir(osp.join('/proc', str(os.getpid()), 'fd')))

   else:
      return -1

class TestFrame(object):
   def __init__(self, tag):
      self.n  = 1
      self.ic = count_open_files()

      # so the excess is stuck at -1, which is a
      # bit more helpful than being stuck at zero
      if self.ic == -1:
         self.ic  =  0

      fd = open('.pending', 'wb')
      fd.write('%s-%s-%s' % (tag, sys.platform, strftime('%Y%m%d%H%M%S', localtime(time()))))
      fd.close()

   def make_msg(self, tag, read_in=False, raise_=False):
      # flush before going deep!
      print                tag + ' out'; sys.stdout.flush()
      print >> sys.stderr, tag + ' err'; sys.stderr.flush()

      os.system('echo %s child out'      % (tag,))
      os.system('echo %s child err 1>&2' % (tag,))

      if read_in:
         n = 0
         for ln in sys.stdin:
            print ln,
            n += 1
         print n

      print '%s excess open files: %d' % (tag, count_open_files() - self.ic)

      if raise_:
         raise RuntimeError(tag)

   def make_delim(self):
      print                '-- %d --' % (self.n,)
      print >> sys.stderr, '++ %d ++' % (self.n,)

      self.n += 1
