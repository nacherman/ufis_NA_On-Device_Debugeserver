# UFIS-NA Tools Reference

This document maps each custom recipe to installed runtime files and usage.

## 1) `ufis-bitstream-manager`

Recipe:

- `project-spec/meta-user/recipes-apps/ufis-bitstream-manager/ufis-bitstream-manager.bb`

Installed files:

- `/usr/bin/ufis_bitstream_server.py`
- `/usr/bin/ufis_load_bit.sh`
- `/lib/systemd/system/ufis-bitstream-manager.service`

Service behavior:

- Starts automatically at boot (`SYSTEMD_AUTO_ENABLE = "enable"`)
- Executes `python3 /usr/bin/ufis_bitstream_server.py`
- Server listens on TCP `5001`
- Each upload is written to `/tmp/received_bitstream.bit`
- Calls `fpgautil -b <file>` after transfer complete

Usage:

```bash
# Check service status
systemctl status ufis-bitstream-manager

# Manual local load helper
ufis_load_bit.sh /path/to/file.bit
```

## 2) `ufis-hw-tools`

Recipe:

- `project-spec/meta-user/recipes-apps/ufis-hw-tools/ufis-hw-tools.bb`

Installed commands:

- `ufis-hw-scan` -> `ufis_hw_scan.py`
- `ufis-reg` -> `ufis_reg.py`
- `ufis-health` -> `ufis_health.py`
- `ufis-mem-bench` -> `ufis_mem_bench.py`
- `ufis-irq-stat` -> `ufis_irq_stat.py`
- `ufis-logic-monitor` -> `ufis_logic_monitor.py`

Runtime dependency declaration:

- `python3-core`
- `python3-json`
- `python3-mmap`
- `python3-io`
- `python3-datetime`

Command details:

### `ufis-hw-scan`

- Scans `/sys/bus/platform/devices/`
- Extracts `compatible` strings and basic address hints
- Output: JSON array

```bash
ufis-hw-scan
```

### `ufis-reg`

- Direct 32-bit register read/write via `/dev/mem`
- Requires root privileges

```bash
# Read
ufis-reg 0x43C00000

# Write
ufis-reg 0x43C00000 0x00000001
```

### `ufis-health`

- Reads XADC values from `/sys/bus/iio/devices/iio:device0`
- Reports temperature, rails, hostname, and load

```bash
ufis-health
ufis-health --json
```

### `ufis-mem-bench`

- Reads a contiguous memory window through `/dev/mem`
- Prints average read throughput in MB/s

```bash
ufis-mem-bench 0x40000000
```

### `ufis-irq-stat`

- Parses `/proc/interrupts`
- Monitor mode prints per-second deltas

```bash
ufis-irq-stat
ufis-irq-stat --json
```

### `ufis-logic-monitor`

- Polls a 32-bit register and reports bit transitions
- Optional mask and interval arguments

```bash
ufis-logic-monitor 0x43C10000
ufis-logic-monitor 0x43C10000 0x000000FF 0.2
```

## 3) `nisl-achermann-branding`

Recipe:

- `project-spec/meta-user/recipes-apps/nisl-achermann-branding/nisl-achermann-branding.bb`

Installed files:

- `/usr/bin/ufis_status`
- `/usr/bin/ufis_net_init`
- `/lib/systemd/system/ufis-net-init.service`

Purpose:

- Provides quick status overview (hostname, uptime, FPGA manager, network, memory)
- Auto-detects the active non-loopback network interface (for example `end0` or `eth0`)
- Boot-time network bootstrap service attempts DHCP and falls back to static IP if no DHCP offer is received.

Network bootstrap defaults:

- Interface: first active non-loopback interface (`UFIS_NET_IF` override supported)
- Fallback IP: `192.168.2.50/24` (`UFIS_STATIC_IP` override supported)

## 4) `base-files` overlay for MOTD

Files:

- `project-spec/meta-user/recipes-core/base-files/base-files_%.bbappend`
- `project-spec/meta-user/recipes-core/base-files/files/motd`

Purpose:

- Provides the custom UFIS-NA login banner by overriding `/etc/motd` inside the `base-files` recipe path.

## 5) Default login credentials (development image)

Defined in `project-spec/configs/rootfs_config` (`CONFIG_ADD_EXTRA_USERS`):

- `root / root`
- `petalinux / petalinux`
- `Nisl_achermann / Nisl_achermann`

These defaults are for development/test and should be rotated for production.

## 6) Layer and platform integration

### Rootfs package selection

Files:

- `project-spec/meta-user/conf/user-rootfsconfig`
- `project-spec/configs/rootfs_config`

These include UFIS packages and selected diagnostics utilities.

### Device tree overlays/custom files

Files:

- `project-spec/meta-user/recipes-bsp/device-tree/device-tree.bbappend`
- `project-spec/meta-user/recipes-bsp/device-tree/files/system-user.dtsi`
- `project-spec/meta-user/meta-xilinx-tools/recipes-bsp/uboot-device-tree/files/system-user.dtsi`

### U-Boot custom config

Files:

- `project-spec/meta-user/recipes-bsp/u-boot/u-boot-xlnx_%.bbappend`
- `project-spec/meta-user/recipes-bsp/u-boot/files/bsp.cfg`
- `project-spec/meta-user/recipes-bsp/u-boot/files/platform-top.h`

### Kernel append

Files:

- `project-spec/meta-user/recipes-kernel/linux/linux-xlnx_%.bbappend`
- `project-spec/meta-user/recipes-kernel/linux/linux-xlnx/bsp.cfg`
