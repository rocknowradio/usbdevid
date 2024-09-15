from datetime import datetime
import json
import os
import platform
import sys
from util.opt import Opt
from sources.web_sources import WebSources

class Data(Opt):
  NAME = 'usbdevid'
  VERSION = '1.0'

  @staticmethod
  def Run(argv):
    data = Data(argv)
    data.run()

  def __init__(self, argv):
    Opt.__init__(self, argv)
    self.records_ = None

  def load_live_data(self):
    # gather data from web sources, unless we're loading local
    if self.is_arg('no-load-live'):
      if self.debug():
        print('load-live: no')
      return
    if self.debug():
      print('load-live: yes')

    sources = WebSources()
    sources.add_sources(['LinuxUSB',
                         'UsbVendor'])
    self.records_ = sources.read(debug=self.debug())
    
    # make name |-separated strings into arrays
    for v_id in self.records_:
      # name
      parts = self.records_[v_id]['name'].split('|')
      self.records_[v_id]['name'] = []
      for part in parts:
        self.records_[v_id]['name'].append(part)
      # devices.name
      for c in range(0, len(self.records_[v_id]['devices'])):
        parts = self.records_[v_id]['devices'][c]['name'].split('|')
        self.records_[v_id]['devices'][c]['name'] = []
        for part in parts:
          self.records_[v_id]['devices'][c]['name'].append(part)

    utc_now = datetime.utcnow()
    out = {
      '__INFO': {
        'source': '%s %s' % (Data.NAME, Data.VERSION),
        'date': '%s' % (utc_now.isoformat()[:19]),
        'os': '%s %s' % (platform.system(), platform.release())
      },
      'data': self.records_ 
    }
 
    # generate USB devices json file
    outfn = self.arg('output')
    if outfn is not None:
      with open(outfn, 'w') as outf:
        outf.write(json.dumps(out, indent=2, sort_keys=True))
    else: 
      if self.debug():
        print(json.dumps(out, indent=2, sort_keys=True))
        
  def load_cached_data(self):
    if not self.is_arg('load-cache'):
      if self.debug():
        print('load-cache: no')
      return
    if self.debug():
      print('load-cache: yes')
  
    infn = self.arg('cache-location')
    if infn is None:
      if self.debug():
        print('load-cache: no')
      return
    try:
      if self.debug():
        print('loading cache from: %s' % (infn))
      with open(infn, 'r') as inf:
        self.records_ = json.load(inf)["data"]
    except Exception as ex:
      if self.debug():
        print('cache load exception: %s' % (ex))
    if self.records_ is None:
      return
    print('records read from cache: %d' % len(self.records_))

  def generate_api(self):
    while True:
      if not self.is_arg('make-api'):
        if self.debug():
          print('make-api: no')
        break
      if self.debug():
        print('make-api: yes')
      api_out_dir = self.arg('api-out-dir')
      if api_out_dir is None:
        if self.debug():
          print('api-out-dir: none')
        break
      if self.debug():
        print('api_out_dir: %s' % api_out_dir)
      if not os.path.isdir(api_out_dir):
        if self.debug():
          print('api_out_dir: %s: not a directory' % api_out_dir)
        break
      if self.debug():
        print('generating api in: %s' % api_out_dir)
      if not self.records_:
        if self.debug():
          print('make-api: no records. either generate from web or load local')
        break

      try:
        h_fn = os.path.join(api_out_dir, 'usbdevid.h')
        with open(h_fn, 'w') as h_f:
          h_f.write('#ifndef __usbdevid_h__\n')
          h_f.write('#define __usbdevid_h__\n')
          h_f.write('\n')
          h_f.write('struct usb_device_t {\n')
          h_f.write('  const char* vendorid;\n')
          h_f.write('  const char* vendor_names[];\n')
          h_f.write('  const char* device_id;\n')
          h_f.write('  const char* device_names[];\n')
          h_f.write('};\n')
          h_f.write('\n')
          h_f.write('/*\n')
          h_f.write(' * Returns the devices table.\n')
          h_f.write(' */\n')
          h_f.write('const struct usbdevice_t*\n')
          h_f.write('usbdevice__get_table(void);\n')
          h_f.write('\n')
          h_f.write('/*\n')
          h_f.write(' * Returns the count of items in devices table.\n')
          h_f.write(' */\n')
          h_f.write('size_t\n')
          h_f.write('usbdevice__get_count(void);\n')
          h_f.write('\n')
          h_f.write('/*\n')
          h_f.write(' * Returns item [0..count) or NULL if not found.\n')
          h_f.write(' */\n')
          h_f.write('const struct usbdevice_t*\n')
          h_f.write('usbdevice__get_item(size_t index);\n')
          h_f.write('\n')
          h_f.write('#endif /* __usbdevid_h__ */\n')
          
        c_fn = os.path.join(api_out_dir, 'usbdevid.c')
        with open(c_fn, 'w') as h_c:
          h_c.write('#include "usbdevid.h"\n')
          h_c.write('\n')
          h_c.write('static const TABLE_SIZE = %d;\n' % len(self.records_))
          h_c.write('\n')
          h_c.write('static struct usb_device_t {\n')
          h_c.write('g__table[%d] = {\n' % len(self.records_)) 
          stop_at = 5
          for v_id in self.records_:
            stop_at -= 1
            if stop_at == 0:
              break
            if len(self.records_[v_id]['devices']) == 0:
              continue
            
            pv, lv = 0, len(self.records_[v_id]['name'])
            for v in range(0, len(self.records_[v_id]['name'])):
              h_c.write('  { "%s",\n' % (v_id))
              if lv == 0:
                h_c.write('  {},\n')
              
              pd, ld = 0, len(self.records_[v_id]['devices'])
              for c in range(0, len(self.records_[v_id]['devices'])):
                h_c.write('    "%s",\n' % (self.records_[v_id]['devices'][c]['id']))
                for name in self.records_[v_id]['devices'][c]['name']:
                  name = name.replace("\"", "\"\"")
                  if pd == 0:
                    if pd == ld - 1:
                      h_c.write('    { "%s" },\n' % (name))
                    else:
                      h_c.write('    { "%s",\n' % (name))
                  elif pd == ld - 1:
                    h_c.write('      "%s" },\n' % (name))
                  else:
                    h_c.write('      "%s",\n' % (name))
                  pd += 1
              
              pv += 1

            '''
            h_c.write('  { "%s",\n' % (v_id))
            if lv == 0:
              h_c.write('  {},\n')
            else:
              for name in self.records_[v_id]['name']:
                name = name.replace("\"", "\"\"")
                if pv == 0:
                  if pv == lv - 1:
                    h_c.write('    { "%s" },\n' % (name))
                  else:
                    h_c.write('    { "%s",\n' % (name))
                elif pv == lv - 1:
                  h_c.write('      "%s" },\n' % (name))
                else:
                  h_c.write('      "%s",\n' % (name))
                pv += 1
            '''

            '''
            pd, ld = 0, len(self.records_[v_id]['devices'])
            for c in range(0, len(self.records_[v_id]['devices'])):
              h_c.write('    "%s",\n' % (self.records_[v_id]['devices'][c]['id']))
              for name in self.records_[v_id]['devices'][c]['name']:
                name = name.replace("\"", "\"\"")
                if pd == 0:
                  if pd == ld - 1:
                    h_c.write('    { "%s" },\n' % (name))
                  else:
                    h_c.write('    { "%s",\n' % (name))
                elif pd == ld - 1:
                  h_c.write('      "%s" },\n' % (name))
                else:
                  h_c.write('      "%s",\n' % (name))
                pd += 1
            '''
            h_c.write('  },\n')

          h_c.write('};\n')
          h_c.write('\n')
          h_c.write('const struct usbdevice_t*\n')
          h_c.write('usbdevice__get_table(void) {\n')
          h_c.write('  return 0;\n')
          h_c.write('}\n')
          h_c.write('\n')
          h_c.write('size_t\n')
          h_c.write('usbdevice__get_count(void) {\n')
          h_c.write('  return _countof(g__table);\n')
          h_c.write('}\n')
          h_c.write('/*\n')
          h_c.write(' * Returns item [0..count) or NULL if not found.\n')
          h_c.write(' */\n')
          h_c.write('const struct usbdevice_t*\n')
          h_c.write('usbdevice__get_item(size_t index) {\n')
          h_c.write('  return NULL;\n')
          h_c.write('}\n')
          h_c.write('\n')

      except Exception as ex:
        if self.debug():
          print('make api exception: %s' % (ex))

      break

  def run(self):
    self.load_live_data()
    self.load_cached_data()

    # generate api
    self.generate_api()

if __name__ == '__main__':
  Data.Run(sys.argv)
