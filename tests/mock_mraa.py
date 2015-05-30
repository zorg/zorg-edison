from mock import Mock
import sys


DIR_OUT = 0
DIR_IN = 1

Aio = Mock()
Gpio = Mock()
Pwm = Mock()
I2c = Mock()


def install_patch():
    from zorg_edison import adaptor

    adaptor.mraa = sys.modules[install_patch.__module__]

def remove_patch():
    from zorg_edison import adaptor

    adaptor.mraa = sys.modules.get("mraa", None)
