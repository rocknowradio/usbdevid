from linux_usb import LinuxUsb
from device_hunt import DeviceHunt

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
    #elif name == 'DeviceHunt':
    #  self.sources_.append({ 'name': 'DeviceHunt',
    #                         'handler': DeviceHunt()})

  def read(self):
    for source in self.sources_:
      records = source['handler'].read()
      self.records_.update(records)

    return self.records_
