#!/usr/bin/env python3
import time
import sys
import json

# ufis_irq_stat.py - Monitors interrupts on the board for AI-agent introspection
def get_irq_stats():
    stats = {}
    try:
        with open('/proc/interrupts', 'r') as f:
            lines = f.readlines()
            
        header = lines[0].split()
        num_cpus = len(header)
        
        for line in lines[1:]:
            parts = line.split()
            if not parts: continue
            
            irq_id = parts[0].strip(':')
            # Extract CPU counts as integers
            counts = []
            for i in range(1, num_cpus + 1):
                try:
                    counts.append(int(parts[i]))
                except (ValueError, IndexError):
                    counts.append(0)
            
            # The remaining parts are the type and device name(s)
            remaining = parts[num_cpus + 1:]
            irq_type = str(remaining[0]) if remaining else "unknown"
            device = " ".join(remaining[1:]) if len(remaining) > 1 else "unknown"
            
            stats[irq_id] = {
                "counts": counts,
                "total": int(sum(counts)),
                "type": irq_type,
                "device": device
            }
    except Exception as e:
        stats["error"] = str(e)
    return stats

def monitor_irq(interval=1.0):
    print(f"Monitoring interrupts (interval {interval}s)... Ctrl+C to stop.")
    prev_stats = get_irq_stats()
    try:
        while True:
            time.sleep(interval)
            curr_stats = get_irq_stats()
            
            diffs = []
            for irq_id, data in curr_stats.items():
                if irq_id != "error" and irq_id in prev_stats:
                    prev_data = prev_stats[irq_id]
                    if isinstance(data, dict) and isinstance(prev_data, dict):
                        delta = int(data.get("total", 0)) - int(prev_data.get("total", 0))
                        if delta > 0:
                            diffs.append((irq_id, delta, data.get("device", "unknown")))
            
            if diffs:
                diffs.sort(key=lambda x: x[1], reverse=True)
                print(f"\n--- {time.strftime('%H:%M:%S')} ---")
                for irq_id, delta, device in diffs:
                    print(f"IRQ {irq_id:3}: {delta:6} events/sec | {device}")
            
            prev_stats = curr_stats
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        print(json.dumps(get_irq_stats(), indent=2))
    else:
        monitor_irq()
