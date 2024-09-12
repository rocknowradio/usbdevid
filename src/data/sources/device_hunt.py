from data_source import WebDataSource

class DeviceHunt(WebDataSource):
  def __init__(self):
    WebDataSource.__init__(self)
  def read(self):
    # https://devicehunt.com/all-usb-vendors
    print('=> DeviceHunt read')
    # self.records_.append({'id': 'DeviceHunt', 'data': 'LinuxUsb data'})
    print('  records: %s' % len(self.records_))
    print('<= DeviceHunt read')
    return self.records_
