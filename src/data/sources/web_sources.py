from linux_usb import LinuxUsb
from device_hunt import DeviceHunt

class WebSources:
  def __init__(self):
    self.records_ = []
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
      print('records: %s' % records)
      print('<= %s::read' % source['name'])
      if False:
        self.records_.append(records) # TODO should merge
      else:
        for record in records:
          self.records_.append(record)
    print('  records: %s' % len(self.records_))
    for record in self.records_:
      print('    %s: %s' % (record['id'], record['data']))
    print('<= WebSources::read')
    return self.records_
