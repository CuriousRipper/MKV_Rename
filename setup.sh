#!/usr/bin/bash

function error_msg() {
    echo "It looks you're missing some prerequisites. MKV_Renamer needs:"
    echo "  * python3"
    echo "  * python3 virtual environment"
    echo "  * python3 development"
    echo "  * the GTK development libraries"
    echo "Would you like to install them? (n/y)"
    echo "This will only work on Debian/Ubuntu/Mint and other distros that use apt"
    read yesno
    if [[ $yesno =~ [yY] ]]; then
      sudo apt install python3-venv python3-pip python3-dev libgtk-3-dev
    else
      exit 1
    fi
}

python3 -m venv lenv
if [[ $? -ne 0 ]]; then
  error_msg
  python3 -m venv lenv
fi

source lenv/bin/activate
pip install -r trb/requirements.txt
if [[ $? -ne 0 ]]; then
  error_msg
  pip install -r trb/requirements.txt
fi

