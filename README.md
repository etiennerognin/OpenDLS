# OpenDLS

An open-source Dynamic Light Scattering device.

## Disclaimer

* This project is at an early stage and is resealsed for research and development only.
* The hardware uses a laser source: handle with appropriate care and protection.

## Description

This is the software part of a full project hosted on https://www.hackster.io/etienner/opendls-an-open-source-dynamic-light-scattering-bff60f. 

At this stage, there are only two files: 
1. 'ArduinoDLS.ino' file to use with Arduino IDE
2. 'OpenDLS.py' python script to collect data from the hardware and analyse it.

## Usage

1. Open 'ArduinoDLS.ino' in the Arduino IDE, compile and upload to the Arduino.
2. Leave the Arduino connected with the USB cable.
3. Open 'OpenDLS.py' with a text editor, set the address of the Arduino.
4. Launch 'OpenDLS.py N' in a terminal, with N is the number of time series to collect from the Arduino. You may need to install some Python libraries.


## License

See [LICENSE](LICENSE).

## Author

Etienne Rognin
