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
        # Confirm the three pin classes are initialized
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

        pin = self.edison.pins["pwm"][5]

        mock_mraa.Pwm.assert_called_with(5)

    def test_write_only_sets_pin_once(self):
        original_pin = Mock()

        self.edison.pins["pwm"][5] = original_pin

        self.edison.servo_write(5, 100)

        self.assertEqual(
            self.edison.pins["pwm"][5],
            original_pin,
            "The pin was overriden even though it had already been initialized"
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
