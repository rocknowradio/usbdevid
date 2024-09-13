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
    outfn = self.arg('output')
  
    sources = WebSources()
    # sources.add_sources(['LinuxUSB', 'UsbVendor'])
    sources.add_sources(['UsbVendor'])

    self.records_ = sources.read(debug=self.debug())

    if self.debug():
      for vid in self.records_:
        record = self.records_[vid]
        if 'devices' in record and len(record['devices']) != 0:
          devices = record['devices']
          for c in range(0, len(devices)):
            print('  %4s:%4s %-40s %s' %
                  (record['id'], devices[c]['id'],
                   record['name'], devices[c]['name']))
        else:
          print('  %4s      %-40s' %
                (record['id'], record['name']))
      print('\n\n')
      j = json.dumps(self.records_)
      print(j)
      
    if not outfn is None:
      with open(outfn, 'w') as outf:
        outf.write(json.dumps(self.records_, indent=2, sort_keys=True))

if __name__ == '__main__':
  Data.Run(sys.argv)
