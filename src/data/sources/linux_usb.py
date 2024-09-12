import httplib2
import StringIO
from data_source import WebDataSource

class LinuxUsb(WebDataSource):
  def __init__(self):
    WebDataSource.__init__(self)

  #
  # data:
  # <vid>: {
  #   'id': vendor_id,
  #   'name': vendor_name,
  #   'devices': [
  #     'id': device_id,
  #     'name': device_name,
  #     'interfaces': [
  #     ]
  #   ]
  # }
  # Since there seems to be no interfaces, we'll ignore it for now.
  #
  def read(self):
    print('=> LinuxUsb read')
    buffer = StringIO.StringIO()
    fail = False
    while not fail:
      try:
        url = 'http://www.linux-usb.org/usb.ids'
        http = httplib2.Http()
        response = http.request(url)
        buffer.write(response[1])
      except ex as Exception:
        fail = True
        print('ex: %s' % str(ex))
      if fail:
        break

      data = buffer.getvalue()
      rows = data.splitlines()
      index = 0
      vendor_started = False
      last_vendor_id = None
      for row in rows:
        if vendor_started:
          # if we have records and we get a blank line, out
          if len(row) == 0:
            break

        index += 1
        
        row = row.rstrip()
        if len(row) == 0:
          continue
        if row[0] == '#':
          continue

        print('+++ [%s]' % (row))
          
        if row.startswith('\t\t'):
          # interface interface_name
          row = row.strip()
          print('   interface: %s' % (row))
        elif row.startswith('\t'):
          # device device_name
          d_row = row.strip()
          # print('  device: %s' % (row))
          parts = d_row.split('\t')
          print('D: parts: d_row=[%s] parts=[%s]' % (d_row, parts))
          if len(parts) != 2:
            pass
          print('D: parts: v_row=[%s] len(parts)=%d', (d_row, len(parts)))
          d_id, d_name = parts[0], parts[1]
          if len(d_id) == 4:
            if vid in self.records_:
              self.records_[last_vendor_id]['devices'].append(
                {'id': d_id, 'name': d_name})
        else:
          # vendor vendor_name
          if not vendor_started:
            vendor_started = True
          v_row = row.strip()
          if len(v_row) <= 6:
            pass
          if v_row[4:5] != '  ':
            pass
          v_id, v_name = v_row[:4], v_row[6:]
          print('V: v_row=[%s] v_id:[%s] v_name:[%s]' % (v_row, v_id, v_name))
          if len(v_id) == 4:
            last_vendor_id = v_id
            if v_id not in self.records_:
              self.records_[v_id] = {'id': v_id, 'name': v_name, 'devices': []}
            else:
              self.records_[v_id]['id'] = v_id
              self.records_[v_id]['name'] = v_name
          # print(' vendor: %s' % (row))
          
      break
    
    print('  records: %s' % len(self.records_))
    print('<= LinuxUsb read')
    return self.records_
