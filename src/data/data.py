from datetime import datetime
import json
import os
import sys
from util.opt import Opt
from sources.web_sources import WebSources

class Data(Opt):
  NAME = 'usbdevid'
  VERSION = '1.0'

  @staticmethod
  def Run(argv):
    data = Data(argv)
    data.run()

  def __init__(self, argv):
    Opt.__init__(self, argv)
    self.records_ = []

  def run(self): 
    sources = WebSources()
    sources.add_sources(['LinuxUSB', 'UsbVendor'])
    self.records_ = sources.read(debug=self.debug())
    
    # make name |-separated strings into arrays
    for v_id in self.records_:
      # name
      parts = self.records_[v_id]['name'].split('|')
      self.records_[v_id]['name'] = []
      for part in parts:
        self.records_[v_id]['name'].append(part)
      # devices.name
      for c in range(0, len(self.records_[v_id]['devices'])):
        parts = self.records_[v_id]['devices'][c]['name'].split('|')
        self.records_[v_id]['devices'][c]['name'] = []
        for part in parts:
          self.records_[v_id]['devices'][c]['name'].append(part)

    utc_now = datetime.utcnow()
    out = {
      '__INFO': {
        'source': '%s %s' % (Data.NAME, Data.VERSION),
        'date': '%s' % (utc_now.isoformat()[:19])
      },
      'data': self.records_ 
    }
 
    outfn = self.arg('output')
    if outfn is not None:
      with open(outfn, 'w') as outf:
        outf.write(json.dumps(out, indent=2, sort_keys=True))
    else: 
      if self.debug():
        print(json.dumps(out, indent=2, sort_keys=True))

if __name__ == '__main__':
  Data.Run(sys.argv)
