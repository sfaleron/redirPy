
from redir import *

from testframe import TestFrame

if __name__ == '__main__':

   fr = TestFrame('py')

   Redir = PythonicRedir

   fr.make_msg('before')

   fr.make_delim()
   with Redir(to=open('output.out', 'wb')):
      fr.make_msg('out')

   fr.make_delim()
   with Redir(ERR, open('output.err', 'wb')):
      fr.make_msg('err')

   fr.make_delim()
   with Redir(to=open('output.out', 'ab')), \
      Redir(ERR, open('output.err', 'ab')):
         fr.make_msg('both, individually')

   fr.make_delim()
   with Redir():
      fr.make_msg('bitbucket')

   fr.make_delim()
   with Redir(IN, open('input.in', 'rb')):
      fr.make_msg('in', True)

   fr.make_delim()
   with Redir(BOTH, open('output.both', 'wb')):
      fr.make_msg('both, together')

   fr.make_delim()
   fr.make_msg('after')
