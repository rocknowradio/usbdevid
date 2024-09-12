import sys

class Opt:
  @staticmethod
  def parse_cmd_line(argv):
    kw = {}
    for c in range(0, len(argv)):
      if argv[c][:2] == '--':
        kv = argv[c][2:].split('=')
        if len(kv) != 0:
          if len(kv) == 1:
            k, v = kv[0], None
          else:
            k, v = kv[0], '='.join(kv[1:])
          if len(k) != 0:
            kw[k] = v
    return kw
    
  def __init__(self, argv):
    self.argv_ = Opt.parse_cmd_line(argv)
    if self.debug():
      print('argv =>')
      for k in self.argv_:
        print('argv[%s]=[%s]' % (k, self.argv_[k]))
      print('<= argv')

  def arg(self, name):
    if name is None or name not in self.argv_:
      return None
    return self.argv_[name]

  def is_arg(self, name):
    if name is None or name not in self.argv_:
      return None
    return True

  def debug(self):
    return self.is_arg('debug')
