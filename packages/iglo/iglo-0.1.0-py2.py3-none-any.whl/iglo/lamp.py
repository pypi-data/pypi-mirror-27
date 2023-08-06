import socket
from iglo.helpers import Helpers

class Lamp(object):
  """
  This represents a lamp to control
  """

  def __init__(self, id, ip, port=8080):
    """
    :type id int:
    :type ip string:
    :type port int:
    :return:
    """
    self.id = id
    self.ip = ip
    self.port = port

  def switch(self, on):
    on_data = 18
    if on:
      on_data = 17
    data = [163, self.id, on_data]
    self._send(data)

  def white(self, whiteness):
    data = [161, self.id, 255 - whiteness, whiteness]
    self._send(data)

  def brightness(self, brightness):
    data = [167, self.id, brightness]
    self._send(data)

  def rgb(self, r, g, b):
    data = [161, self.id, r, g, b]
    self._send(data)

  def _send(self, data):
    data_bytes = bytearray(Helpers.int_array_to_byte_array([-2, -17, len(data) + 1]))
    data_bytes.extend(Helpers.int_array_to_byte_array(data))
    checksum = 0
    for i in data:
      checksum += i
    data_bytes.append((checksum % 256) ^ 255)
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.send(data_bytes)
    sock.close()
    sock = None

  def close(self):
    self.socket.close()
