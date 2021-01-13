# metar-taf-upy
ESP32+METAR/TAF+4x20 display WX station with live data

## About
Displays METAR and TAF from a specific weather station on a 40x4 HD44780 LCD display with a PCF8574 backpack board.

Using [python_lcd](https://github.com/dhylands/python_lcd) for display comms.

## Install


Get the Micropython firmware on your Espressif microcontroller. [For ESP32](https://micropython.org/download/esp32/). If using a WROGER board, make sure you get the SPIRAM firmware version.

Add the 2.4 WiFi SSID(s) and password(s) to wifi.dat.

Add the ICAO code for the station to monitor (only one allowed).

Open a CLI window on the directory the files are in. Enter the script files to the board's root directory with [ampy])(https://github.com/scientifichackers/ampy) and the corresponding serial port. Shown are the commands for Windows and COM6:

```
ampy -p COM6 -b 112500 boot.py
ampy -p COM6 -b 112500 main.py
ampy -p COM6 -b 112500 ICAO.dat
ampy -p COM6 -b 112500 wifi.dat
ampy -p COM6 -b 112500 esp8266_i2c_lcd.py
ampy -p COM6 -b 112500 lcd_api.py
```

Connect the PCF8574 backpack board to the ESP microcontroller:

* VCC -> 5V
* GND -> GND
* SDA -> GPIO21
* SCL -> GPIO22

Reset the board, and go build an enclosure! ;)
