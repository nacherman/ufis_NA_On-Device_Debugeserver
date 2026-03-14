#!/usr/bin/env python3
import socket
import os
import subprocess
import time

PORT = 5001
TEMP_BIT = "/tmp/received_bitstream.bit"

def load_bitstream(path):
    print(f"Loading bitstream: {path}")
    try:
        # Use fpgautil to load the bitstream
        # PetaLinux 2020+ uses fpgautil
        result = subprocess.run(["fpgautil", "-b", path], capture_output=True, text=True)
        if result.returncode == 0:
            print("Bitstream loaded successfully.")
        else:
            print(f"Error loading bitstream: {result.stderr}")
    except Exception as e:
        print(f"Exception during bitstream load: {e}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', PORT))
        s.listen()
        print(f"Bitstream Server listening on port {PORT}...")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connection from {addr}")
                with open(TEMP_BIT, 'wb') as f:
                    while True:
                        data = conn.recv(4096)
                        if not data:
                            break
                        f.write(data)
                print("Bitstream received. Triggering load...")
                load_bitstream(TEMP_BIT)

if __name__ == "__main__":
    start_server()
