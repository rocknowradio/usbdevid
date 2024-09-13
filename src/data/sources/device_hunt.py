from data_source import WebDataSource

class DeviceHunt(WebDataSource):
  def __init__(self):
    WebDataSource.__init__(self)

  @staticmethod
  def id():
    return 'DeviceHunt'

  def read(self):
    # https://devicehunt.com/all-usb-vendors
    print('-+- => %s read' % DeviceHunt.id())
    
    # pass

    print('-+-   records: %s' % len(self.records_))
    print('-+- <= %s read' % DeviceHunt.id())
    return self.records_
