# Zorg Edison

The `zorg-edison` module wraps the mraa library created by intel for interacting
with IO pins on the Edison microcontroller. While the Python bindings for mraa
work great on their own, the benefit of using Zorg is
that we have already created many of the drivers you
needed for using sensors and output devices. Zorg also
implements multiprocessing so that tasks such as reading and
writing from sensors are non-blocking, allowing you to take full
advantage of multi-processor boards like the Intel Edison.

**Zorg also creates a REST API for you :)**

## Installation

```
pip install zorg-edison
```

## [Documentation](http://zorg-edison.readthedocs.org/)
