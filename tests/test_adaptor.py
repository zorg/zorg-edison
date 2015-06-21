from mock import Mock

from . import mock_mraa
mock_mraa.install_patch()

from unittest import TestCase
from zorg_edison import Edison


class ConstructorTests(TestCase):

    def setUp(self):
        super(ConstructorTests, self).setUp()

        self.edison = Edison({})

    def test_pins(self):
        # Confirm the four pin classes are initialized
        self.assertTrue(
            "analog" in self.edison.pins,
            "Analog pins were not initialized"
        )
        self.assertTrue(
            "digital" in self.edison.pins,
            "Digital pins were not initialized"
        )
        self.assertTrue(
            "pwm" in self.edison.pins,
            "PWM pins were not initialized"
        )
        self.assertTrue(
            "i2c" in self.edison.pins,
            "I2C bus was not initialized"
        )

        # Confirm that no pins are connected by default
        self.assertEqual(
            len(self.edison.pins["analog"]),
            0,
            "There were analog pins initialized by default"
        )
        self.assertEqual(
            len(self.edison.pins["digital"]),
            0,
            "There were digital pins initialized by default"
        )
        self.assertEqual(
            len(self.edison.pins["pwm"]),
            0,
            "There were PWM pins initialized by default"
        )
        self.assertTrue(
            self.edison.pins["i2c"] is None,
            "There were I2C pins initialized by default"
        )


class ServoTests(TestCase):

    def setUp(self):
        super(ServoTests, self).setUp()

        self.edison = Edison({})

    def test_write_sets_up_pin(self):
        self.edison.servo_write(5, 100)

        self.assertTrue(
            5 in self.edison.pins["pwm"],
            "The pin was not initialized"
        )

        mock_mraa.Pwm.assert_called_with(5)

    def test_write_only_sets_pin_once(self):
        original_pin = Mock()

        self.edison.pins["pwm"][5] = original_pin

        self.edison.servo_write(5, 100)

        self.assertEqual(
            self.edison.pins["pwm"][5],
            original_pin,
            "The pin was overridden even though it had already been initialized"
        )

    def test_write_enables_pin(self):
        pin = Mock()
        self.edison.pins["pwm"][5] = pin

        self.edison.servo_write(5, 100)

        pin.enable.assert_called_with(True)

    def test_write_sets_period(self):
        pin = Mock()
        self.edison.pins["pwm"][5] = pin

        self.edison.servo_write(5, 100)

        pin.period_us.assert_called_with(7968)

    def test_write_min_width(self):
        pin = Mock()
        self.edison.pins["pwm"][5] = pin

        self.edison.servo_write(5, 0)

        pin.pulsewidth_us.assert_called_with(600)

    def test_write_mid_width(self):
        pin = Mock()
        self.edison.pins["pwm"][5] = pin

        self.edison.servo_write(5, 90)

        pin.pulsewidth_us.assert_called_with(1600)

    def test_write_max_width(self):
        pin = Mock()
        self.edison.pins["pwm"][5] = pin

        self.edison.servo_write(5, 180)

        pin.pulsewidth_us.assert_called_with(2600)


class DigitalTests(TestCase):

    def setUp(self):
        super(DigitalTests, self).setUp()

        self.edison = Edison({})

    def test_write_sets_up_pin(self):
        self.edison.digital_write(5, 100)

        self.assertTrue(
            5 in self.edison.pins["digital"],
            "The pin was not initialized"
        )

        mock_mraa.Gpio.assert_called_with(5)

    def test_write_only_sets_pin_once(self):
        original_pin = Mock()

        self.edison.pins["digital"][5] = original_pin

        self.edison.digital_write(5, 100)

        self.assertEqual(
            self.edison.pins["digital"][5],
            original_pin,
            "The pin was overridden even though it had already been initialized"
        )

    def test_write_sets_direction(self):
        pin = Mock()

        self.edison.pins["digital"][5] = pin

        self.edison.digital_write(5, 100)

        pin.dir.assert_called_with(mock_mraa.DIR_OUT)

    def test_write_works(self):
        pin = Mock()

        self.edison.pins["digital"][5] = pin

        self.edison.digital_write(5, 100)

        pin.write.assert_called_with(100)


class AnalogTests(TestCase):

    def setUp(self):
        super(AnalogTests, self).setUp()

        self.edison = Edison({})

    def test_read_sets_up_pin(self):
        self.edison.analog_read(5)

        self.assertTrue(
            5 in self.edison.pins["analog"],
            "The pin was not initialized"
        )

        mock_mraa.Aio.assert_called_with(5)

    def test_read_only_sets_pin_once(self):
        original_pin = Mock()

        self.edison.pins["analog"][5] = original_pin

        self.edison.analog_read(5)

        self.assertEqual(
            self.edison.pins["analog"][5],
            original_pin,
            "The pin was overridden even though it had already been initialized"
        )

    def test_read_calls_read(self):
        pin = Mock()

        self.edison.pins["analog"][5] = pin

        self.edison.analog_read(5)

        pin.read.assert_called_with()

    def test_read_returns_value(self):
        pin = Mock()

        pin.read.return_value = 100

        self.edison.pins["analog"][5] = pin

        value = self.edison.analog_read(5)

        self.assertEqual(
            value,
            100,
            "The value from read() was not returned"
        )


class I2CTests(TestCase):

    def setUp(self):
        super(I2CTests, self).setUp()

        self.edison = Edison({})

    def test_write_sets_up_pin(self):
        self.edison.i2c_write(0, 0x3e, 0xFF, 0)

        self.assertTrue(
            self.edison.pins["i2c"] is not None,
            "The address was not initialized"
        )

        mock_mraa.I2c.assert_called_with(0)

    def test_write_only_sets_pin_once(self):
        original_pin = Mock()

        self.edison.pins["i2c"] = original_pin

        self.edison.i2c_write(0, 0x3e, 0x00, 1)

        self.assertEqual(
            self.edison.pins["i2c"],
            original_pin,
            "The address was overridden even though" +
            " it had already been initialized"
        )

    def test_write_works(self):
        pin = Mock()

        self.edison.pins["i2c"] = pin

        self.edison.i2c_write(0, 0x00, 0xFF, 0)

        pin.writeReg.assert_called_with(0xFF, 0)
