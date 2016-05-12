
from redir import *

from testframe import TestFrame


if __name__ == '__main__':

   fr = TestFrame('catchsys')

   Redir = SystemRedir

   fr.make_msg('before')

   fr.make_delim()
   with Redir(to=open('output.out', 'wb'), catch=True, reraise=False), \
      Redir(ERR, open('output.err', 'wb')):
         fr.make_msg('out/err/out', raise_=True)

   fr.make_delim()
   with Redir(to=open('output.out', 'ab')), \
      Redir(ERR, open('output.err', 'ab'), catch=True, reraise=False):
         fr.make_msg('out/err/err', raise_=True)

   fr.make_delim()
   with Redir(ERR, open('output.err', 'ab'), catch=True, reraise=False), \
      Redir(to=open('output.out', 'ab')):
         fr.make_msg('err/out/err', raise_=True)

   fr.make_delim()
   with Redir(ERR, open('output.err', 'ab')), \
      Redir(to=open('output.out', 'ab'), catch=True, reraise=False):
         fr.make_msg('err/out/out', raise_=True)

   # both

   fr.make_delim()
   with Redir(to=open('output.out', 'wb'), catch=True, reraise=False), \
      Redir(ERR, open('output.err', 'wb'), catch=True, reraise=False):
         fr.make_msg('out/err/both', raise_=True)

   fr.make_delim()
   with Redir(ERR, open('output.err', 'ab'), catch=True, reraise=False), \
      Redir(to=open('output.out', 'ab'), catch=True, reraise=False):
         fr.make_msg('err/out/both', raise_=True)

   # both, inner reraises

   fr.make_delim()
   with Redir(to=open('output.out', 'wb'), catch=True, reraise=False), \
      Redir(ERR, open('output.err', 'wb'), catch=True):
         fr.make_msg('out/err/reraise', raise_=True)

   fr.make_delim()
   with Redir(ERR, open('output.err', 'ab'), catch=True, reraise=False), \
      Redir(to=open('output.out', 'ab'), catch=True):
         fr.make_msg('err/out/reraise', raise_=True)

   fr.make_delim()
   fr.make_msg('after')
