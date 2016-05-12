
from redir import *

from testframe import TestFrame

if __name__ == '__main__':

   fr = TestFrame('nullsys')

   Redir = SystemRedir

   fr.make_msg('before')

   fr.make_delim()
   with Redir(to=open('output.out', 'wb'), nullmode=True):
      fr.make_msg('out')

   fr.make_delim()
   with Redir(ERR, open('output.err', 'wb'), nullmode=True):
      fr.make_msg('err')

   fr.make_delim()
   with Redir(to=open('output.out', 'ab'), nullmode=True), \
      Redir(ERR, open('output.err', 'ab'), nullmode=True):
         fr.make_msg('both, individually')

   fr.make_delim()
   with Redir(nullmode=True):
      fr.make_msg('bitbucket')

   fr.make_delim()
   with Redir(BOTH, open('output.both', 'wb'), nullmode=True):
      fr.make_msg('both, together')

   fr.make_delim()
   fr.make_msg('after')
