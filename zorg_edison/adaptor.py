from zorg.adaptor import Adaptor
import sys

try:
    import mraa
except ImportError:
    sys.stderr.write("Could not load the Python bindings for libmraa\n")
    mraa = None


MIN_PULSE_WIDTH = 600
MAX_PULSE_WIDTH = 2600
MAX_PERIOD = 7968


class Edison(Adaptor):

    def __init__(self, options):
        super(Edison, self).__init__(options)

        self.pins = {
            "digital": {},
            "analog": {},
            "pwm": {},
            "i2c": None,
        }

    def servo_write(self, pin, degrees):
        pulse_width = MIN_PULSE_WIDTH + \
            (degrees / 180.0) * (MAX_PULSE_WIDTH - MIN_PULSE_WIDTH)

        self.pwm_write(pin, int(pulse_width), MAX_PERIOD)

    def pwm_write(self, pin_number, value, period):
        if not pin_number in self.pins["pwm"]:
            pin = mraa.Pwm(pin_number)
            self.pins["pwm"][pin_number] = pin
        else:
            pin = self.pins["pwm"][pin_number]

        pin.period_us(period)

        # The pin needs to be enabled if it wasn't already
        pin.enable(True)

        pin.pulsewidth_us(value)

    def digital_write(self, pin_number, value):
        if not pin_number in self.pins["digital"]:
            pin = mraa.Gpio(pin_number)
            self.pins["digital"][pin_number] = pin
        else:
            pin = self.pins["digital"][pin_number]

        pin.dir(mraa.DIR_OUT)
        pin.write(value)

    def digital_read(self, pin_number):
        if not pin_number in self.pins["digital"]:
            pin = mraa.Gpio(pin_number)
            self.pins["digital"][pin_number] = pin
        else:
            pin = self.pins["digital"][pin_number]

        pin.dir(mraa.DIR_IN)

        return pin.read()

    def analog_read(self, pin_number):
        if not pin_number in self.pins["analog"]:
            pin = mraa.Aio(pin_number)
            self.pins["analog"][pin_number] = pin
        else:
            pin = self.pins["analog"][pin_number]

        return pin.read()

    def i2c_write(self, pin_number, address, register, data):
        """
        Requires a pin number, device address, a register to write to,
        and the data to write to the register.
        """
        if not self.pins["i2c"]:
            bus = mraa.I2c(pin_number)
            self.pins["i2c"] = bus
        else:
            bus = self.pins["i2c"]

        bus.address(address)
        bus.writeReg(register, data)
