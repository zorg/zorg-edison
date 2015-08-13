# `class Edison(options)`
Takes a single dictionary parameter called `options`.

## `servo_write(pin, degrees)`
An internal method that will be called by a driver class
to write a value in degrees to a servo connected to a
specified pin on the Intel Edison.

## `pwm_write(pin_number, value, period)`
An internal method that will be called by a driver class
to write a pwm signal to a specified pin on the Intel Edison.

## `digital_write(pin_number, value)`
An internal method that will be called by a driver class
to write a digital value to a specified pin on the Intel
Edison.

## `analog_read(pin_number)`
An internal method that will be called by a driver class
to return the value at an analog pin on the Intel Edison.

## `i2c_write(pin_number, address, register, data)`
An internal method that will be called by a driver class
to write a value to the I2C bus on the Intel Edison.
