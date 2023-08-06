from cutecare.backends import BluetoothInterface
import logging

_HANDLE_GPIO_DATA = 0x07
_LOGGER = logging.getLogger(__name__)

class CuteCareGPIOJDY8(object):

    def __init__(self, mac, backend, adapter='hci0'):
        self._mac = mac
        self._bt_interface = BluetoothInterface(backend, adapter)

    def name(self):
        return 'CuteCare GPIO JDY-08'

    def set_gpio(self, pin, state):
        with self._bt_interface.connect(self._mac) as connection:
            connection.write_handle(_HANDLE_GPIO_DATA, "E7F" + str(pin) + "01" if state else "E7F" + str(pin) + "00")
            return None