#!/usr/bin/env python3
import sys
import os
import struct
import mmap

# ufis_reg.py - Low-level direct register access tool for AI-agent hardware testing
def read_mem(addr):
    try:
        page_size = os.sysconf('SC_PAGESIZE')
        page_addr = addr & ~(page_size - 1)
        offset = addr - page_addr
        
        with open('/dev/mem', 'r+b') as f:
            mm = mmap.mmap(f.fileno(), page_size, offset=page_addr)
        # Use mm[offset:offset+4] slicing but ensure compatibility
        val = struct.unpack('<I', mm[offset:offset+4])[0]
        mm.close()
        return val
    except Exception as e:
        print(f"Error reading address 0x{addr:08X}: {e}")
        return None

def write_mem(addr, val):
    try:
        page_size = os.sysconf('SC_PAGESIZE')
        page_addr = addr & ~(page_size - 1)
        offset = addr - page_addr
        
        with open('/dev/mem', 'r+b') as f:
            mm = mmap.mmap(f.fileno(), page_size, offset=page_addr)
        mm[offset:offset+4] = struct.pack('<I', val)
        mm.close()
        return True
    except Exception as e:
        print(f"Error writing to address 0x{addr:08X}: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ufis_reg <addr> [val]")
        print("Example: ufis_reg 0x43C00000 (Read)")
        print("Example: ufis_reg 0x43C00000 0x00000001 (Write)")
        sys.exit(1)
    
    try:
        addr = int(sys.argv[1], 16)
        if len(sys.argv) == 3:
            val = int(sys.argv[2], 16)
            if write_mem(addr, val):
                print(f"Wrote 0x{val:08X} to 0x{addr:08X}")
        else:
            val = read_mem(addr)
            if val is not None:
                print(f"0x{addr:08X}: 0x{val:08X}")
    except ValueError:
        print("Invalid address or value format. Use hex (e.g., 0x43C00000).")
        sys.exit(1)
