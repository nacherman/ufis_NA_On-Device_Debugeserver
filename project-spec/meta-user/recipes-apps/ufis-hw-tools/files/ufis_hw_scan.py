#!/usr/bin/env python3
import os
import json

# ufis_hw_scan.py - Scans AXI platform devices for AI-agent introspection
def get_platform_devices():
    base_path = '/sys/bus/platform/devices/'
    devices = []
    if not os.path.exists(base_path):
        return devices
        
    for d in os.listdir(base_path):
        dev_path = os.path.join(base_path, d)
        try:
            # Look for compatible string in Device Tree node
            comp_path = os.path.join(dev_path, 'of_node', 'compatible')
            if os.path.exists(comp_path):
                with open(comp_path, 'rb') as f:
                    compatible = f.read().decode('utf-8').strip('\0').split('\0')
                
                # Try to find memory resource
                reg_path = os.path.join(dev_path, 'of_node', 'reg')
                addr = "N/A"
                if os.path.exists(reg_path):
                    # Simplistic address extraction from node name often works on Zynq
                    if '.' in d:
                        addr = "0x" + d.split('.')[-1]

                devices.append({
                    'name': d,
                    'compatible': compatible[0] if compatible else 'unknown',
                    'addr': addr,
                    'path': dev_path
                })
        except Exception as e:
            continue
    return devices

if __name__ == "__main__":
    devs = get_platform_devices()
    # Sort by address if possible
    devs.sort(key=lambda x: x['addr'] if x['addr'] != "N/A" else "ZZZZ")
    print(json.dumps(devs, indent=2))
