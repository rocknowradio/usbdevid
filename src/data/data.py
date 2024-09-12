import os
import sys
from util.opt import Opt
from sources.web_sources import WebSources

class Data(Opt):
  @staticmethod
  def Run(argv):
    data = Data(argv)
    data.run()

  def __init__(self, argv):
    Opt.__init__(self, argv)
    self.records_ = []

  def run(self):
    print('=> Run')
    sources = WebSources()
    sources.add_source('LinuxUSB')
    sources.add_source('DeviceHunt')

    records = sources.read()

    print('  records: %s' % len(self.records_))
    for record in self.records_:
      print('    %s' % (record))
    print('<= Run')

if __name__ == '__main__':
  Data.Run(sys.argv)
