#! /usr/bin/env python

import logtool, re
from cfgstack import CfgStack

RE_VAR = re.compile (r"\$\{([A-Za-z0-9._]+:?[A-Za-z0-9._]*)\}")

class CfgSet (object):

  _stack = None

  @logtool.log_call
  def __init__ (self, fnames, dirs = None, exts = None):
    self._stack = [CfgStack (f, dirs = dirs, exts = exts).data for f in fnames]

  @logtool.log_call
  def _expand_vars (self, ctx, v):
    while True:
      m = RE_VAR.search (v)
      if not m:
        break
      n = m.group (1) # Variable name
      r = self.value (ctx + [n]) # Replacement value
      if isinstance (r, (basestring, int, long, float, complex)):
        # print "Pre: ", v
        v = "%s%s%s" % (v[:m.start(0)], r, v[m.end(0):])
        # print "Interim: ", v
      else: # Scummy, fails complex emebeds, kinda handles the tuples
        # print "Complex: ", r, type (r)
        v = r
        break
    return v

  @logtool.log_call (log_args = False)
  def _value_lookup (self, cfgset, ctx, k):
    sl = [cfgset["DEFAULT"],] if "DEFAULT" in cfgset else []
    d = cfgset
    for s in ctx:
      if not d.has_key (s):
        break
      d = d[s]
      sl.insert (0, d)
    for d in sl:
      # print "Look for -- K: ", k , "D: ", d, "V: [%s]" % d.get (k)
      if d.has_key (k):
        # print "\tFound %s / %s in %s" % (k, sl, d
        # print "\tFound: ", d.get (k)
        return d.get (k)
    # print "Failed to find %s / %s" % (k, sl)
    raise ValueError

  @logtool.log_call
  def _get_value (self, ctx, k):
    for d in self._stack:
      try:
        return self._value_lookup (d, ctx, k)
      except ValueError:
        pass
    raise ValueError ("FAULT: No definition found for: %s" % k)

  @logtool.log_call
  def value (self, k):
    # Different semantics from get(): exception on missing key
    # Note that only simple values will be interpolated.
    if isinstance (k, basestring):
      sl = k.split ("/")
    elif isinstance (k, (list, tuple)):
      sl = k
    else:
      raise TypeError ("type(k) must be string, list or tuple.")
    key = sl[-1]
    ctx = sl[:-1]
    # print "CTX: ", ctx
    # print "Key: ", key
    v = self._get_value (ctx, key)
    # print "RC: ", v
    # Complex types aren't expanded
    if isinstance (v, list): # So it satisfies the % operator
      v = tuple (v)
    elif isinstance (v, basestring): # Substitute ${VAR} value
      v = self._expand_vars (ctx, v)
    # print "Final: ", v
    return v
