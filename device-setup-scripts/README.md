# IQT Labs: EdgeTech Device Setup

## PinePhone Installation Instructions

### Install OS
1. [Install Tow-Boot](https://tow-boot.org/devices/pine64-pinephonePro.html)
2. Start phone in *USB Mass Storage* mode by holding the volume up button at startup before and during the second vibration. The LED will turn **blue** if done successfully. In this mode, the phone will work like a USB drive when connected to a host computer.
3. Flash [mobian image](https://images.mobian.org/pinephonepro/weekly/) with [Etcher](https://www.balena.io/etcher/) or *dd* command [(detailed instructions: https://wiki.pine64.org/wiki/PinePhone_Installation_Instructions)](https://wiki.pine64.org/wiki/PinePhone_Installation_Instructions)
4. Default login is `1234`
5. Power Settings
    - Settings -> Power -> Automatic Suspend OFF
    - Settings -> Power -> Show Battery Percentage ON
6. Set hostname `hostnamectl set-hostname HOSTNAME`
6. [optional] Cellular Setup
    - Insert SIM
    - Settings -> Mobile Data ON -> "4G LTE Contract vzwinternet"
    - Settings -> Data Roaming ON
    - Reboot and confirm the above settings are still set. Sometimes it takes an additional reboot/set for them to be saved.

### Install EdgeTech Prerequisites

The setup scripts contained in this folder are intended to bring a device from a base install of the OS up to a configuration ready for installation of an EdgeTech-compatible tool.

The setup script can be run from a shortend URL:

 `bash <(curl -fsSL https://short.iqt.org/pinephonepro)`
