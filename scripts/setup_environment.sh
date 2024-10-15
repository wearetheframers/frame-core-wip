#!/bin/bash

# Determine the OS and select the appropriate requirements file
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    cp requirements-linux.txt requirements.txt
elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* ]]; then
    cp requirements-win.txt requirements.txt
else
    echo "Unsupported OS type: $OSTYPE"
    exit 1
fi
