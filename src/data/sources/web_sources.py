from linux_usb import LinuxUsb
from device_hunt import DeviceHunt

class WebSources:
  def __init__(self):
    self.records_ = {}
    self.sources_ = []

  def add_source(self, name):
    if name == 'LinuxUSB':
      self.sources_.append({ 'name': 'LinuxUSB', 'handler': LinuxUsb()})
    elif name == 'DeviceHunt':
      self.sources_.append({ 'name': 'DeviceHunt', 'handler': DeviceHunt()})

  def read(self):
    print('=> WebSources::read')
    for source in self.sources_:
      print('=> %s::read' % source['name'])
      records = source['handler'].read()
      print('[*] records: %d' % len(records))
      # print('<= %s::read' % source['name'])
      # TODO should merge ?
      self.records_.update(records)
      print('[*] self.records_: %d' % len(self.records_))
      print('<= %s::read' % source['name'])
    print('  records: %d' % len(self.records_))
    #for vid in self.records_:
    #  print('    %s: %s' % (vid, record[vid]))
    print('<= WebSources::read')
    return self.records_
