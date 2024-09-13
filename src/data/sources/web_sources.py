from linux_usb import LinuxUsb
from usb_vendor import UsbVendor

class WebSources:
  def __init__(self):
    self.records_ = {}
    self.sources_ = []

  def add_sources(self, names):
    for name in names:
      self.add_source(name)

  def add_source(self, name):
    if name == 'LinuxUSB':
      self.sources_.append({ 'name': 'LinuxUSB',
                             'handler': LinuxUsb()})
    if name == 'UsbVendor':
      self.sources_.append({ 'name': 'UsbVendor',
                             'handler': UsbVendor()})

  def read(self, debug=False):
    for source in self.sources_:
      records = source['handler'].read(debug)
      self.records_.update(records)

    return self.records_
