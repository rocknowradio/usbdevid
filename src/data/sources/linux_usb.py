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

      vendor_started = False
      last_vendor_id = None
      for row in rows:
        if vendor_started:
          # if we have records and we get a blank line, out
          if len(row) == 0:
            break

        row = row.rstrip()
        if len(row) == 0:
          continue
        if row[0] == '#':
          continue

        if row.startswith('\t\t'):
          # interface interface_name
          row = row.strip()
          print('   interface: %s' % (row))
        elif row.startswith('\t'):
          # device device_name
          d_row = row.strip()
          if len(d_row) > 6:
            if d_row[4:6] == '  ':
              d_id, d_name = d_row[:4], d_row[6:]
              if len(d_id) == 4:
                if last_vendor_id in self.records_:
                  self.records_[last_vendor_id]['devices'].append(
                    {'id': d_id, 'name': d_name})
        else:
          # vendor vendor_name
          if not vendor_started:
            vendor_started = True
          v_row = row.strip()
          if len(v_row) > 6:
            if v_row[4:6] == '  ':
              v_id, v_name = v_row[:4], v_row[6:]
              if len(v_id) == 4:
                last_vendor_id = v_id
                if v_id not in self.records_:
                  self.records_[v_id] = {'id': v_id, 'name': v_name, 'devices': []}
                else:
                  self.records_[v_id]['id'] = v_id
                  self.records_[v_id]['name'] = v_name
          
      break
    
    print('  records: %d' % len(self.records_))
    print('<= LinuxUsb read')
    return self.records_
