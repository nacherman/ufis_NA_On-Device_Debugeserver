#!/usr/bin/env python3
import time
import os
import mmap
import struct
import sys
import json

# ufis_logic_monitor.py - Monitors bitfield changes in specific hardware registers
# Designed for AI agents to track state transitions in custom IP

def monitor_bits(addr, mask=0xFFFFFFFF, interval=0.1):
    page_size = os.sysconf('SC_PAGESIZE')
    page_addr = addr & ~(page_size - 1)
    offset = addr - page_addr
    
    print(f"Monitoring 0x{addr:08X} (mask: 0x{mask:08X}, interval: {interval}s)...")
    
    try:
        with open('/dev/mem', 'r+b') as f:
            mm = mmap.mmap(f.fileno(), page_size, offset=page_addr)
            
            last_val = struct.unpack('<I', bytes(mm[offset:offset+4]))[0] & mask
            print(f"Initial State: 0x{last_val:08X}")
            
            while True:
                time.sleep(interval)
                curr_val = struct.unpack('<I', bytes(mm[offset:offset+4]))[0] & mask
                if curr_val != last_val:
                    # Report change
                    change_type = "INCREASED" if curr_val > last_val else "DECREASED"
                    # Count bits set in XOR to detect single bit changes
                    xor_val = curr_val ^ last_val
                    if bin(xor_val).count('1') == 1:
                        bit_pos = xor_val.bit_length() - 1
                        change_type = f"BIT {bit_pos} {'SET' if (curr_val >> bit_pos) & 1 else 'CLEARED'}"
                    
                    now = time.strftime('%H:%M:%S')
                    print(f"[{now}] Change: 0x{last_val:08X} -> 0x{curr_val:08X} ({change_type})")
                    last_val = curr_val
                    
    except KeyboardInterrupt:
        print("\nStopped.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ufis-logic-monitor <addr> [mask] [interval]")
        sys.exit(1)
        
    addr = int(sys.argv[1], 16)
    mask = int(sys.argv[2], 16) if len(sys.argv) > 2 else 0xFFFFFFFF
    interval = float(sys.argv[3]) if len(sys.argv) > 3 else 0.1
    
    monitor_bits(addr, mask, interval)
