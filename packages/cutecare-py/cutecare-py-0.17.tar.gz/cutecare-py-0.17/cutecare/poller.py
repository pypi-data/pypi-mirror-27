from datetime import datetime, timedelta
from threading import Lock
from cutecare.backends import BluetoothInterface
import logging

_HANDLE_READ_SENSOR_DATA = 0x25
_LOGGER = logging.getLogger(__name__)

class CuteCarePollerCC41A(object):

    def __init__(self, mac, backend, adapter='hci0'):
        self._mac = mac
        self._bt_interface = BluetoothInterface(backend, adapter)

    def name(self):
        return 'CuteCare CC41A DIY Sensor'

    def parameter_value(self):
        with self._bt_interface.connect(self._mac) as connection:
            raw_data = connection.read_handle_listen(_HANDLE_READ_SENSOR_DATA)
            _LOGGER.debug('Received result for handle %s: %s', \
                          _HANDLE_READ_SENSOR_DATA, self._format_bytes(raw_data))
            return raw_data[0] * 256 + raw_data[1];

    @staticmethod
    def _format_bytes(raw_data):
        """Prettyprint a byte array."""
        return ' '.join([format(c, "02x") for c in raw_data]).upper()
