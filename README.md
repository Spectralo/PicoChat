# PicoChat

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Raspberry Pi](https://img.shields.io/badge/-RaspberryPi-C51A4A?style=for-the-badge&logo=Raspberry-Pi)

Pico chat is a little *Python* program that create an acess point with a __chat server__ ✨ \
Its'a website so everyone can acess it if they're connected on the wifi !

## How to run it on your Pico W

*Note : it should work on every circuitpython wifi board but I only tested with a Pico W*

Supported boards :
- Pico W (RP2040)

### 1) Install adafruit-http

- Using circup

    ```bash
    circup install adafruit-http
    ```
- Manually

    Download the latest release from [here](https://circuitpython.org/libraries) and copy the `adafruit_http` folder to your `lib` folder.

### 2) Upload the code to your board

- Launch the upload.py script

    ```bash
    python3 upload.py
    ```
- Or copy the `code.py` file to your board

### 3) Enjoy ✨ (And contribute ?)

- Connect to the wifi network `PicoChat`
- Open your browser and go to `192.168.1.10`
