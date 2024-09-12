import sys

class Opt:
  @staticmethod
  def parse_cmd_line(argv):
    kw = []
    for c in range(0, len(argv)):
      if argv[c][:2] == '--':
        kv = argv[c][2:].split('=')
        if len(kv) != 0:
          if len(kv) == 1:
            k, v = kv[0], None
          else:
            k, v = kv[0], '='.join(kv[1:])
          if len(k) != 0:
            kw.append([k, v])
    return kw
    
  def __init__(self, argv):
    self.argv_ = Opt.parse_cmd_line(argv)
    if self.debug():
      print('argv =>')
      for c in range(0, len(self.argv_)):
        print('argv[%s]=[%s]' % (self.karg(c), self.varg(self.karg(c))))
      print('<= argv')

  def kvarg(self, index):
    if index is None:
      return None
    if index < 0 or index > len(self.argv_):
      return None
    return self.argv_[index][0], self.argv_[index][1]

  def karg(self, index):
    if index is None:
      return None
    if index < 0 or index > len(self.argv_):
      return None
    return self.argv_[index][0]

  def varg(self, name):
    if name is None:
      return None
    for c in range(0, len(self.argv_)):
      if self.kvarg(c)[0] == name:
        return self.kvarg(c)[1]
    return None

  def debug(self):
    for c in range(0, len(self.argv_)):
      if self.kvarg(c)[0] == 'debug':
        return True
    return False
