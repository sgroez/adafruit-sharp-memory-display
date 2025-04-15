# Adafruit Sharp Memory Display

Python program to render linux /dev/fb0 framebuffer on adafruit 400x240 sharp memory display

## Wiring

| Display | Rasperri Pi   |
| ------- | ------------- |
| VIN     | 3.3V          |
| 3v3     | Not connected |
| GND     | GND           |
| CLK     | 11 SCLK       |
| DI      | 10 MOSI       |
| CS      | 22            |

## Preparation

### Enable SPI

- sudo raspi-config
- select Interface Options
- select SPI
- confirm by selecting yes

### Setup Framebuffer Without Display Attached

- open /boot/firmware/cmdline.txt
- add `video=HDMI-A-1:720x480M@30D`

### Install Adafruit Sharp Memory Display Library

```python
pip3 install adafruit-circuitpython-sharpmemorydisplay

```

## Run Program

```
sudo path_to_venv/bin/python3 __main__.py
```

## Add System Service To Start On Boot

```
cp sharp_display.service /lib/systemd/system/
```

- open /lib/systemd/system/sharp_display.service
- change ExecStart python3 path to path_to_venv/bin/python3
- change ExecStart executable path to the localy cloned repo

```
sudo systemctl daemon-reload
sudo systemctl enable sharp_display.service
sudo reboot
```

# Sources

## Display

https://learn.adafruit.com/adafruit-sharp-memory-display-breakout/python-usage

https://github.com/adafruit/Adafruit_CircuitPython_SharpMemoryDisplay

## Service

https://github.com/ian-antking/cardkb
