#!/usr/bin/env python3
import os
import json
import sys

# ufis_health.py - Comprehensive board health report for AI agents via XADC and SysFS
def get_xadc_data():
    base_path = "/sys/bus/iio/devices/iio:device0"
    if not os.path.exists(base_path):
        return {"error": "XADC driver not found (check kernel config/dtb)"}

    results = {}
    # Mapping of channel names to SysFS file names
    channels = {
        "temperature": "in_temp0_raw",
        "vccint": "in_voltage0_vccint_raw",
        "vccaux": "in_voltage1_vccaux_raw",
        "vccpcre": "in_voltage2_vccpcre_raw",
    }
    
    # Scale and offset files are usually common or per-channel
    # temp = (raw + offset) * scale
    # voltage = raw * scale
    
    try:
        temp_raw = int(open(os.path.join(base_path, "in_temp0_raw")).read().strip())
        temp_offset = float(open(os.path.join(base_path, "in_temp0_offset")).read().strip())
        temp_scale = float(open(os.path.join(base_path, "in_temp0_scale")).read().strip())
        results["temperature_c"] = round(float((temp_raw + temp_offset) * temp_scale / 1000.0), 2)
        
        vint_raw = int(open(os.path.join(base_path, "in_voltage0_vccint_raw")).read().strip())
        vint_scale = float(open(os.path.join(base_path, "in_voltage0_vccint_scale")).read().strip())
        results["vccint_v"] = round(float(vint_raw * vint_scale / 1000.0), 3)
        
        vaux_raw = int(open(os.path.join(base_path, "in_voltage1_vccaux_raw")).read().strip())
        vaux_scale = float(open(os.path.join(base_path, "in_voltage1_vccaux_scale")).read().strip())
        results["vccaux_v"] = round(float(vaux_raw * vaux_scale / 1000.0), 3)
    except Exception as e:
        results["error"] = str(e)
        
    return results

def get_system_load():
    try:
        load = os.getloadavg()
        return {"1min": load[0], "5min": load[1], "15min": load[2]}
    except:
        return {"1min": "N/A", "5min": "N/A", "15min": "N/A"}

if __name__ == "__main__":
    report = {
        "hostname": os.uname().nodename,
        "xadc": get_xadc_data(),
        "load": get_system_load()
    }
    
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        print(json.dumps(report, indent=2))
    else:
        print(f"--- UFIS-NA Board Health Report ---")
        print(f"Hostname:    {report['hostname']}")
        if "error" in report["xadc"]:
            print(f"XADC Error:  {report['xadc']['error']}")
        else:
            print(f"Temperature: {report['xadc'].get('temperature_c', 'N/A')} C")
            print(f"VCCINT:      {report['xadc'].get('vccint_v', 'N/A')} V")
            print(f"VCCAUX:      {report['xadc'].get('vccaux_v', 'N/A')} V")
        
        load_val = report['load'].get('1min', 'N/A')
        print(f"System Load: {load_val} (1m)")
