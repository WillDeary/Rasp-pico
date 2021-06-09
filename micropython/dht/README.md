
#DHT
There are two files here the DHT11 interface and the main.py file.

There is an in-depth tutorial on: https://how2electronics.com/interfacing-dht11-temperature-humidity-sensor-with-raspberry-pi-pico/
(Not written by me)

Import the sensor
`import dht`

Initilize the DHT11 senor with
`sensor = DHT11(PIN)`

Get temperature
`sensor.temperature`

Get humidity
`sensor.humidity`

You may also need to look out for the two exceptions:
` InvalidChecksum`
and
`InvalidPulseCount`

Without catching these exceptions your DHT11 sensor may just stop giving you the readings.


