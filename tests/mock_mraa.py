from mock import Mock
import sys


Aio = Mock()
Gpio = Mock()
Pwm = Mock()


def install_patch():
    from zorg_edison import adaptor

    adaptor.mraa = sys.modules[install_patch.__module__]

def remove_patch():
    from zorg_edison import adaptor

    adaptor.mraa = sys.modules.get("mraa", None)
