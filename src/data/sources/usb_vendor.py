import httplib2
import json
import StringIO
from data_source import WebDataSource

class UsbVendor(WebDataSource):
  def __init__(self):
    WebDataSource.__init__(self)

  @staticmethod
  def id():
    return 'UsbVendor'

  def read(self, debug):
    if debug:
      print('=> %s read' % UsbVendor.id())
  
    buffer = StringIO.StringIO()
    fail = False
    offset, count, total_records = 0, 10, -1
    all_data = []
    while not fail:
      try:
        url_fmt = 'https://api-usbvendor-dev.nssup.net/Public/FindDevices?Offset=%d&Count=%d&SortField=Id&SortDirection=ASC'
        url = url_fmt % (offset, count)
        print('url: %s' % url)
        # request will have also the total
        http = httplib2.Http()
        response = http.request(url)
        buffer.write(response[1])
        
        data = buffer.getvalue()
        print('data: %s' % (data))
        j = json.loads(data)
        if total_records == -1:
          if 'Total' in j:
            total_records = j['Total']
        print('total_records: %d' % total_records)
        
        # data
        if 'Data' in j:
          partial_data = j['Data']
          # if we don't have data, bail out
          if len(partial_data) == 0:
            break
          print('Data contains %d entries' % len(partial_data))
          all_data.append(partial_data)
        
        # update offset and count
        offset += count
        count += count
        if offset > total_records:
          print('offset=%d > total_records=%d: done' % (offset, total_records))
          break
        print('\n')
        
      except Exception as ex:
        fail = True
        print('ex: %s' % str(ex))
      print('while loop done. fail:%s all_data:%d' % ('yes' if fail else 'no', len(all_data)))
      if fail:
        break


    if debug:
      print('records: %d' % len(self.records_))
      print('<= %s read' % UsbVendor.id())

    return self.records_
