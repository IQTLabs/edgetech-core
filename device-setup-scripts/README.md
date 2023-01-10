# IQT Labs: EdgeTech Project Setup Scripts

## PinePhone Installation Instructions

### Install OS
1. [Install Tow-Boot](https://tow-boot.org/devices/pine64-pinephonePro.html)
2. Start phone in *USB Mass Storage* mode by holding the volume up button at startup before and during the second vibration. The LED will turn **blue** if done successfully. In this mode, the phone will work like a USB drive when connected to a host computer.
3. Flash [mobian image](https://images.mobian.org/pinephonepro/weekly/) with [Etcher](https://www.balena.io/etcher/) or *dd* command [(detailed instructions: https://wiki.pine64.org/wiki/PinePhone_Installation_Instructions)](https://wiki.pine64.org/wiki/PinePhone_Installation_Instructions)

### Install EdgeTech Prerequisites

The setup scripts contained in this folder are intended to bring a device from a base install of the OS up to a configuration ready for installation of an EdgeTech-compatible tool.

Our installation instructions will usually point from shortened links.  The scripts can be accessed here.


Supported devices currently are:
  - [PinePhone Pro](./pinephone-pro_setup.sh)   |   `curl -fsSL https://short.iqt.org/pinephonepro | sh`
