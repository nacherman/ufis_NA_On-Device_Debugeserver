#!/bin/sh
if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_bitstream>"
    exit 1
fi
fpgautil -b "$1"
