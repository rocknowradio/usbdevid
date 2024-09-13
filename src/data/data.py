import json
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

    self.records_ = sources.read()

    for vid in self.records_:
      record = self.records_[vid]
      if 'devices' in record and len(record['devices']) != 0:
        devices = record['devices']
        for c in range(0, len(devices)):
          if c < 10:
            print('  %4s:%4s %-40s %s' % (record['id'], devices[c]['id'], record['name'], devices[c]['name']))
    #print('\n\n')
    j = json.dumps(self.records_, indent=4, sort_keys=True)
    print(j)
    
    print('<= Run')

if __name__ == '__main__':
  Data.Run(sys.argv)
