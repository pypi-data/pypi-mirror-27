MCP342x
=======

A Python module to support Microchip MCP342x analogue to digital
converters. The devices use the I2C bus. For the low level I2C
protocol this module depends on SMBus.

Supported devices
-----------------

*   MCP3422: 2 channel, 12, 14, 16, or 18 bit
*   MCP3423: 2 channel, 12, 14, 16, or 18 bit
*   MCP3424: 4 channel, 12, 14, 16, or 18 bit
*   MCP3426: 2 channel, 12, 14, or 16 bit
*   MCP3427: 2 channel, 12, 14, or 16 bit
*   MCP3428: 4 channel, 12, 14, or 16 bit

The MCP3422 and MCP3426 use I2C address 0x68, all other devices can be
configured to use any address in the range 0x68 - 0x6F (inclusive).
