# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2020 Mark Roberts for Adafruit Industries
# SPDX-FileCopyrightText: 2021 James Carr
#
# SPDX-License-Identifier: MIT
"""
`adafruit_displayio_sh1107`
================================================================================

DisplayIO driver for SH1107 monochrome displays


* Author(s): Scott Shawcroft, Mark Roberts (mdroberts1243), James Carr

Implementation Notes
--------------------

**Hardware:**

* `Adafruit FeatherWing 128 x 64 OLED - SH1107 128x64 OLED <https://www.adafruit.com/product/4650>`_

**Software and Dependencies:**

* Adafruit CircuitPython (version 5+) firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import displayio
from micropython import const

__version__ = "1.2.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_DisplayIO_SH1107.git"


DISPLAY_OFFSET_ADAFRUIT_FEATHERWING_OLED_4650 = const(0x60)
"""
The hardware display offset to use when configuring the SH1107 for the
`Adafruit Featherwing 128x64 OLED <https://www.adafruit.com/product/4650>`_

.. code-block::

    from adafruit_displayio_sh1107 import SH1107, DISPLAY_OFFSET_ADAFRUIT_FEATHERWING_OLED_4650

    # Simplest constructor, assumes it is an Adafruit FeatherWing 128x64 OLED
    display = SH1107(bus, width=128, height=64,
        display_offset=DISPLAY_OFFSET_ADAFRUIT_FEATHERWING_OLED_4650)
    # Or as it's the default
    display = SH1107(bus, width=128, height=64)
"""

DISPLAY_OFFSET_PIMORONI_MONO_OLED_PIM374 = const(0x00)
"""
The hardware display offset to use when configuring the SH1107 for the
`Pimoroni Mono 128x128 OLED <https://shop.pimoroni.com/products/1-12-oled-breakout>`_

.. code-block::

    from adafruit_displayio_sh1107 import SH1107, DISPLAY_OFFSET_PIMORONI_MONO_OLED_PIM374

    # Constructor for the Pimoroni Mono 128x128 OLED
    display = SH1107(bus, width=128, height=128,
        display_offset=DISPLAY_OFFSET_PIMORONI_MONO_OLED_PIM374)
"""


# Sequence from sh1107 framebuf driver formatted for displayio init
_INIT_SEQUENCE = (
    b"\xae\x00"  # display off, sleep mode
    b"\xdc\x01\x00"  # display start line = 0 (POR = 0)
    b"\x81\x01\x2f"  # contrast setting = 0x2f
    b"\x21\x00"  # vertical (column) addressing mode (POR=0x20)
    b"\xa0\x00"  # segment remap = 1 (POR=0, down rotation)
    b"\xcf\x00"  # common output scan direction = 15 (0 to n-1 (POR=0))
    b"\xa8\x01\x7f"  # multiplex ratio = 128 (POR)
    b"\xd3\x01\x60"  # set display offset mode = 0x60
    b"\xd5\x01\x51"  # divide ratio/oscillator: divide by 2, fOsc (POR)
    b"\xd9\x01\x22"  # pre-charge/dis-charge period mode: 2 DCLKs/2 DCLKs (POR)
    b"\xdb\x01\x35"  # VCOM deselect level = 0.770 (POR)
    b"\xb0\x00"  # set page address = 0 (POR)
    b"\xa4\x00"  # entire display off, retain RAM, normal status (POR)
    b"\xa6\x00"  # normal (not reversed) display
    b"\xaf\x00"  # DISPLAY_ON
)


class SH1107(displayio.Display):
    """
    SSD1107 driver for use with DisplayIO

    :param bus: The bus that the display is connected to.
    :param int width: The width of the display. Maximum of 128
    :param int height: The height of the display. Maximum of 128
    :param int rotation: The rotation of the display. 0, 90, 180 or 270.
    :param int display_offset: The display offset that the first column is wired to.
        This will be dependent on the OLED display and two displays with the
        same dimensions could have different offsets. This defaults to
        `DISPLAY_OFFSET_ADAFRUIT_FEATHERWING_OLED_4650`
    """

    def __init__(
        self,
        bus,
        display_offset=DISPLAY_OFFSET_ADAFRUIT_FEATHERWING_OLED_4650,
        **kwargs
    ):
        init_sequence = bytearray(_INIT_SEQUENCE)
        init_sequence[19] = display_offset
        super().__init__(
            bus,
            init_sequence,
            **kwargs,
            color_depth=1,
            grayscale=True,
            pixels_in_byte_share_row=True,  # in vertical (column) mode
            data_as_commands=True,  # every byte will have a command byte preceeding
            set_vertical_scroll=0xD3,  # TBD -- not sure about this one!
            brightness_command=0x81,
            single_byte_bounds=True,
            # for sh1107 use column and page addressing.
            #                lower column command = 0x00 - 0x0F
            #                upper column command = 0x10 - 0x17
            #                set page address     = 0xB0 - 0xBF (16 pages)
            SH1107_addressing=True,
        )
        self._is_awake = True  # Display starts in active state (_INIT_SEQUENCE)

    @property
    def is_awake(self):
        """
        The power state of the display. (read-only)

        True if the display is active, False if in sleep mode.
        """
        return self._is_awake

    def sleep(self):
        """
        Put display into sleep mode

        The display uses < 5uA in sleep mode
        Sleep mode does the following:
        1) Stops the oscillator and DC-DC circuits
        2) Stops the OLED drive
        3) Remembers display data and operation mode active prior to sleeping
        4) The MP can access (update) the built-in display RAM
        """
        if self._is_awake:
            self.bus.send(int(0xAE), "")  # 0xAE = display off, sleep mode
            self._is_awake = False

    def wake(self):
        """
        Wake display from sleep mode
        """
        if not self._is_awake:
            self.bus.send(int(0xAF), "")  # 0xAF = display on
            self._is_awake = True