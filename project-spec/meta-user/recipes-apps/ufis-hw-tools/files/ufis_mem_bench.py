#!/usr/bin/env python3
import time
import os
import mmap
import struct
import sys

# ufis_mem_bench.py - Measures memory throughput using /dev/mem to simulate AXI data paths
def bench_mem(addr, size_mb=10, iterations=5):
    size_bytes = size_mb * 1024 * 1024
    page_size = os.sysconf('SC_PAGESIZE')
    page_addr = addr & ~(page_size - 1)
    offset = addr - page_addr
    
    total_size = size_bytes + offset
    
    print(f"Benchmarking 0x{addr:08X} with {size_mb}MB ({iterations} iterations)...")
    
    try:
        with open('/dev/mem', 'r+b') as f:
            mm = mmap.mmap(f.fileno(), total_size, offset=page_addr)
            
            # Warm up
            _ = bytes(mm[offset:offset+1024])
            
            read_speeds = []
            for i in range(iterations):
                start = time.perf_counter()
                # Use bytes() to trigger fast C-level copy/slicing
                _ = bytes(mm[offset:offset+size_bytes])
                end = time.perf_counter()
                dt = end - start
                read_speeds.append(size_mb / dt)
                
            avg_read = sum(read_speeds) / iterations
            print(f"Average Read: {avg_read:.2f} MB/s")
            
            mm.close()
            return {"read_mbps": round(float(avg_read), 2)}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    target_addr = 0x40000000 # Default Zynq DDR base for Many designs
    if len(sys.argv) > 1:
        target_addr = int(sys.argv[1], 16)
    
    bench_mem(target_addr)
