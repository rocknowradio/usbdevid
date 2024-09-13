import urllib.request
import json
from .data_source import WebDataSource

def to_hex(i):
  try:
    return hex(i)[2:]
  except:
    return None

class UsbVendor(WebDataSource):
  def __init__(self):
    WebDataSource.__init__(self)

  @staticmethod
  def id():
    return 'UsbVendor'

  def read(self, debug):
    if debug:
      print('=> %s read' % UsbVendor.id())
  
    fail = False
    offset, count, total_records = 0, 1000, -1
    all_data = []
    offset = 0
    while not fail:
      try:
        url_fmt = 'https://api-usbvendor-dev.nssup.net/Public/FindDevices?Offset=%d&Count=%d&SortField=Id&SortDirection=ASC'
        url = url_fmt % (offset, count)
        #print('url: %s' % url)
        # request will have also the total
        req = urllib.request.urlopen(url)
        data = req.read().decode(errors="ignore")      
        # print('data: %s' % (data))
        
        j = json.loads(data)
        if total_records == -1:
          if 'Total' in j:
            total_records = j['Total']
        #print('total_records: %d' % total_records)
        
        # data
        if 'Data' in j:
          partial_data = j['Data']
          # if we don't have data, bail out
          if len(partial_data) == 0:
            break
          #print('Data contains %d entries' % len(partial_data))
          all_data.append(partial_data)
        
        # update offset and count
        offset += count
        if offset > total_records:
          #print('offset=%d > total_records=%d: done' % (offset, total_records))
          break
      except Exception as ex:
        fail = True
        print('ex: %s' % str(ex))
        
    read_records = 0
    for c in range(0, len(all_data)):
      read_records += len(all_data[c])
    #print('++ while loop done. fail:%s all_data:%d read_records:%d' % ('yes' if fail else 'no', len(all_data), read_records))

    l = len(all_data)
    for i in range(0, len(all_data)):
      for j in range(0, len(all_data[i])):
        e = all_data[i][j]
        while True:
          d_id = to_hex(e['Identifier'] if 'Identifier' in e else None)
          d_name = e['Name'] if 'Name' in e else None
          # print('d_id=%s type(d_id)=%s d_name=%s' % (d_id, type(d_id), d_name))
          if 'Vendor' in e:
            if e['Vendor'] is not None:
              v_id = to_hex(e['Vendor']['Identifier'] if 'Identifier' in e['Vendor'] else None)
              v_name = e['Vendor']['Name'] if 'Name' in e['Vendor'] else None
              #print('v_id=%s type(v_id)=%s v_name=%s' % (v_id, type(v_id), v_name))
          if v_id is not None:
            v_id = v_id.zfill(4)
            if v_id not in self.records_:
              self.records_[v_id] = {'id': v_id, 'name': v_name, 'devices': []}
            if d_id is not None:
              d_id = d_id.zfill(4)
              self.records_[v_id]['devices'].append({'id': d_id, 'name': d_name})
          break
    
    if debug:
      print('records: %d' % len(self.records_))
      print('records: %s' % self.records_)
      print('<= %s read' % UsbVendor.id())

    return self.records_
