
# System mode was adapted from a very detailed and thorough stackoverflow comment
# by JF Sebastian: http://stackoverflow.com/a/22434262/4279

# A notable change is the call to fdopen was removed, as per (and as tested!)
# http://homepage.ntlworld.com/jonathan.deboynepollard/FGA/redirecting-standard-io.html

# Redirection without the context managing may be obtained by calling the enter() and exit() methods directly.


import os
import sys

import traceback

from collections import Sequence, Set

IN, OUT, ERR = [1<<i for i in range(3)]
BOTH = OUT|ERR

D = dict( ((IN, 'stdin'), (OUT, 'stdout'), (ERR, 'stderr')) )


class RedirBase(object):
   def _init(self, frm, to, catch, reraise, do_not_close, nullmode):
      if frm&IN and frm&BOTH:
         raise ValueError('streams must all be in the same direction')

      if not frm&(IN|BOTH):
         raise ValueError('no streams selected')

      self.catch    = catch
      self.reraise  = reraise
      self.nullmode = nullmode

      self.to       = open(os.devnull, 'rb' if frm&IN else 'wb') if to is None else to

      # do_not_close is coerced when NULL is opened internally
      self.do_not_close = do_not_close and to

   def _enter(self):
      return self.to

   def _handle_exceptions(self, typ, val, tb):
      catch = self.catch
      if catch and tb:
         if callable(catch):
            result = catch(typ, val, tb)
            if isinstance(result, basestring):
               self.to.write(result)
         else:
            traceback.print_exc(file=self.to)

   def _exit(self):
      if not self.do_not_close:
         self.to.close()

      return not self.reraise

   def enter(self):
      return self.__enter__()

# not only for child processes! also redirects previously grabbed references to the streams, handy!
# workaround with the pythonic version is straightforward but awkward.
class SystemRedir(RedirBase):
   def __init__(self, frm=OUT, to=None, catch=False, reraise=True, do_not_close=False, nullmode=False):
      self._init(frm, to, catch, reraise, do_not_close, nullmode)

      if not self.nullmode:
         self.frm = [ {'frm': getattr(sys, D[i])} for i in (IN,OUT,ERR) if frm&i ]

   def __enter__(self):
      if not self.nullmode:
         for d in self.frm:
            d['fd' ] = fd  = d['frm'].fileno()
            d['cpy'] = cpy = os.dup(fd)

            d['frm'].flush()
            os.dup2(self.to.fileno(), fd)

      return self._enter()

   def __exit__(self, *args):
      self._handle_exceptions(*args)
      return self.exit()

   def exit(self):
      if not self.nullmode:
         for d in self.frm:
            d['frm'].flush()
            os.dup2(d['cpy'], d['fd'])

            os.close(d['cpy'])

      return self._exit()

class PythonicRedir(RedirBase):
   def __init__(self, frm=OUT, to=None, mode='redir', catch=False, reraise=True, do_not_close=False, nullmode=False):
      self._init(frm, to, catch, reraise, do_not_close, nullmode)

      if not self.nullmode:
         self.frm = dict( [(i, getattr(sys, D[i])) for i in (IN,OUT,ERR) if frm&i ] )

   def __enter__(self):
      if not self.nullmode:
         for k,v in self.frm.items():
            v.flush()
            setattr(sys, D[k], self.to)

      return self._enter()

   def __exit__(self, *args):
      self._handle_exceptions(*args)
      return self.exit()

   def exit(self):
      if not self.nullmode:
         for k,v in self.frm.items():
            setattr(sys, D[k], v)

      return self._exit()

# only makes sense for output modes with PythonicRedir
class Multiplexer(object):
   def __init__(self, descs):
      self.descs = descs
   def write(self, s):
      for desc in self.descs:
         desc.write(s)
      self.flush()
   # only writes to the first descriptor if seq is a generator!
   def writelines(self, seq):
      for desc in self.descs:
         desc.writelines(seq)
      self.flush()
   def flush(self):
      for desc in self.descs:
         desc.flush()
   def close(self):
      for desc in self.descs:
         desc.close()

__all__ = ('PythonicRedir', 'SystemRedir', 'IN', 'OUT', 'ERR', 'BOTH', 'Multiplexer')
