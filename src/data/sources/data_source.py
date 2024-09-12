class WebDataSource:
  #
  # data:
  # <vid>: {
  #   'id': vendor_id,
  #   'name': [vendor_names],
  #   'devices': [
  #     { 'id': device_id,
  #       'name': [device_names],
  #       'interfaces': [
  #       ]
  #     }
  #   ]
  # }
  # Since there seems to be no interfaces, we'll ignore it for now.
  #

  def __init__(self):
    self.records_ = {}

  @staticmethod
  def id():
    return None

  def read(self):
    return None
