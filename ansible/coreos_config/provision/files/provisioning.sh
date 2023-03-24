#!/bin/bash

FCOSDISK=/dev/sda1,
sudo coreos-installer install --architecture=aarch64 -i config.ign $FCOSDISK

FCOSEFIPARTITION=$(lsblk $FCOSDISK -J -oLABEL,PATH  | jq -r '.blockdevices[] | select(.label == "EFI-SYSTEM")'.path)
mkdir /tmp/FCOSEFIpart
sudo mount $FCOSEFIPARTITION /tmp/FCOSEFIpart
pushd /tmp/FCOSEFIpart
VERSION=$(curl https://api.github.com/repos/pftf/RPi4/releases/latest -s | jq .name -r)  # use latest one from https://github.com/pftf/RPi4/releases
sudo curl -LO https://github.com/pftf/RPi4/releases/download/${VERSION}/RPi4_UEFI_Firmware_${VERSION}.zip
sudo unzip RPi4_UEFI_Firmware_${VERSION}.zip
sudo rm RPi4_UEFI_Firmware_${VERSION}.zip
popd
sudo umount /tmp/FCOSEFIpart