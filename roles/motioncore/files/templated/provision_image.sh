#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

[[ -d /tmp/FCOSEFIpart ]] && rm -rf /tmp/FCOSEFIpart
FCOSDISK=/dev/sda
sudo coreos-installer install --architecture=aarch64 -s stable -i ${SCRIPT_DIR}/config.ign $FCOSDISK