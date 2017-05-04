#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P  )
cd "$parent_path"

sudo apt-get update
sudo apt-get install kpartx
sudo apt-get install qemu-kvm
sudo apt-get install qemu-user-static
pip3 install -r setup_files/requirements.txt
