from .linux_usb import LinuxUsb
from .usb_vendor import UsbVendor

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
    # TODO: https://linux-hardware.org/ 
    #       https://bsd-hardware.info/


  def       read(self, debug=False):
    for source in self.sources_:
      records = source['handler'].read(debug)

      if len(self.records_) == 0:
        self.records_.update(records)
      else:
        for recid in records:
          record = records[recid]
          # check if record is in self.records_
          v_id = record['id']
          if v_id not in self.records_:
            # print('new record from vendor: %s' % v_id)
            self.records_[v_id] = record
          else:
            # exists; how to merge?
            # append device name if does not exists
            v_name = self.records_[v_id]['name']
            exists = False
            names = v_name.split('|')
            for name in names:
              if name.startswith(record['name']):
                exists = True
                break
            if not exists:
              print('new name from vendor: %s' % record['name'])
              self.records_[v_id]['name'] += '|%s' % record['name']
              
            # devices
            for i in range(0, len(record['devices'])):
              exists = False
              device = record['devices'][i]
              
              for j in range(0, len(self.records_[v_id]['devices'])):
                if self.records_[v_id]['devices'][j]['id'] == device['id']:
                  exists = True
                  break
                  
              if not exists:
                #print('new device from vendor: %s' % device)
                self.records_[v_id]['devices'].append({'id': device['id'], 'name': device['name']})
              else:
                for j in range(0, len(self.records_[v_id]['devices'])):
                  if self.records_[v_id]['devices'][j]['id'] == device['id']:
                    exists = False
                    names = self.records_[v_id]['devices'][j]['name'].split('|')
                    for name in names:
                      if name.startswith(device['name']):
                        exists = True
                        break
                    if not exists:
                      #print('new name for device:%s : %s' % (self.records_[v_id]['devices'][j], device['name']))
                      self.records_[v_id]['devices'][j]['name'] += '|%s' % device['name']

    return self.records_
