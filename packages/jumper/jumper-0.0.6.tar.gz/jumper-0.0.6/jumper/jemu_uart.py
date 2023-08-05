"""
:copyright: (c) 2017 by Jumper Labs Ltd.
:license: Apache 2.0, see LICENSE.txt for more details.
"""
import os
import os.path
import serial


class JemuUart(object):
    _uart_device = None
    _uart_device_path = None

    def __init__(self, uart_device_path):
        self._uart_device = None
        self._uart_device_path = uart_device_path
        self._buffer = b''
        try:
            os.unlink(uart_device_path)
        except:
            pass

    def remove(self):
        if not os.path.exists(self._uart_device_path):
            return

        if not os.path.islink(self._uart_device_path):
            raise Exception(self._uart_device_path + ' not symbolic link')

        os.unlink(self._uart_device_path)

    def open(self):
        if not os.path.islink(self._uart_device_path):
            raise Exception(self._uart_device_path +
                            ' not found or not symbolic link')

        self._uart_device = serial.Serial(self._uart_device_path, timeout=0.2)

    def close(self):
        if self._uart_device:
            self._uart_device.close()

    def read_line(self, line_seperator=b'\r\n'):
        while line_seperator not in self._buffer:
            temp_data = self._uart_device.read(1024)
            self._buffer += temp_data
        line_length = self._buffer.find(line_seperator) + len(line_seperator)
        data = self._buffer[:line_length]
        self._buffer = self._buffer[line_length:]
        return data

    def read(self):
        self._buffer += self._uart_device.read(1024)
        data = self._buffer
        self._buffer = b''
        return data

    def wait_until_uart_receives(self, data):
        while data not in self._buffer:
            temp_data = self._uart_device.read(1024)
            self._buffer += temp_data
            # if temp_data != '':
            #     print(temp_data)
                
        tmp = self._buffer
        self._buffer = b''
        return tmp

    def write(self, data):
        self._uart_device.write(data)
