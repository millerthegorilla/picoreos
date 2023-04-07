#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

is_mounted() {
    mount | awk -v DIR="$1" '{if ($3 == DIR) { exit 0}} ENDFILE{exit -1}'
}

[[ -d /tmp/FCOSEFIpart ]] && rm -rf /tmp/FCOSEFIpart
FCOSDISK=/dev/sda
sudo coreos-installer install --architecture=aarch64 -i ${SCRIPT_DIR}/config.ign $FCOSDISK
sleep 5
FCOSEFIPARTITION=$(lsblk ${FCOSDISK} -J -oLABEL,PATH  | jq -r '.blockdevices[] | select(.label == "EFI-SYSTEM")'.path)
mkdir /tmp/FCOSEFIpart
sudo mount $FCOSEFIPARTITION /tmp/FCOSEFIpart
pushd /tmp/FCOSEFIpart
VERSION=$(curl https://api.github.com/repos/pftf/RPi4/releases/latest -s | jq .name -r)  # use latest one from https://github.com/pftf/RPi4/releases
sudo curl -LO https://github.com/pftf/RPi4/releases/download/${VERSION}/RPi4_UEFI_Firmware_${VERSION}.zip
sudo unzip RPi4_UEFI_Firmware_${VERSION}.zip
sudo rm RPi4_UEFI_Firmware_${VERSION}.zip
popd
if is_mounted /tmp/FCOSEFIpart; then
    sudo umount /tmp/FCOSEFIpart
fi
find /tmp/ -name "coreos-installer*" -maxdepth 1 -type=d exec sudo rm -rf {} +
[[ -d /tmp/FCOSEFIpart ]] && sudo rm -rf /tmp/FCOSEFIpart