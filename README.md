# UFIS-NA On-Device Debug Server (PetaLinux)

PetaLinux project for the UFIS-NA Zynq platform, providing:

- Remote FPGA bitstream upload/loading on TCP port `5001`
- On-device hardware diagnostics tools for AXI/platform introspection
- UFIS-specific branding and status utilities

Project owner: `Nils_Achermann`

## Repository layout

- `project-spec/meta-user/` - custom Yocto layer with UFIS recipes
- `project-spec/configs/` - PetaLinux project and rootfs configuration
- `project-spec/hw-description/` - hardware handoff (`system.xsa`, init files)
- `images/linux/` - build outputs (`BOOT.BIN`, `image.ub`, `rootfs.*`, etc.)

## UFIS custom packages included in rootfs

- `nisl-achermann-branding`
- `ufis-bitstream-manager`
- `ufis-hw-tools`
- Utility packages (for diagnostics workflows): `iperf3`, `jq`, `tmux`, `usbutils`, `stress-ng`, `python3-psutil`, `python3-pyyaml`

## Default login credentials (development image)

Configured via `project-spec/configs/rootfs_config`:

- `root / root`
- `petalinux / petalinux`
- `Nisl_achermann / Nisl_achermann`

These are development defaults and should be changed for production deployments.

## Architecture and workflow diagrams

### 1) System architecture

Shows host interfaces (USB-serial, Ethernet, bitstream client) and target-side services/tools.

![UFIS system architecture](docs/diagrams/svg/system_architecture.svg)

### 2) Bitstream upload workflow

From TCP upload on port `5001` to `fpgautil -b` FPGA programming.

![Bitstream upload workflow](docs/diagrams/svg/bitstream_upload_workflow.svg)

### 3) Hardware diagnostics workflow

How UFIS tools map to `/sys`, `/proc`, and `/dev/mem` data paths.

![Hardware diagnostics workflow](docs/diagrams/svg/hw_diagnostics_workflow.svg)

### 4) Serial/USB to Ethernet debug workflow

End-to-end debug flow for console, USB checks, and network troubleshooting.

![Serial USB to Ethernet debug workflow](docs/diagrams/svg/serial_usb_to_ethernet_debug.svg)

### 5) Runtime boot and service workflow

Boot path through `systemd`, service startup, and user tools.

![Runtime boot flow](docs/diagrams/svg/runtime_boot_flow.svg)

More diagrams and PNG fallbacks: [`docs/UFIS_ARCHITECTURE.md`](docs/UFIS_ARCHITECTURE.md)  
Complete audited file map: [`docs/UFIS_META_USER_FILEMAP.md`](docs/UFIS_META_USER_FILEMAP.md)

## Quick command reference

| Command | Purpose | Example |
| --- | --- | --- |
| `ufis-hw-scan` | Enumerate platform devices and compatible strings | `ufis-hw-scan` |
| `ufis-reg` | Read/write memory-mapped registers via `/dev/mem` | `ufis-reg 0x43C00000` |
| `ufis-health` | Board health report (XADC + load) | `ufis-health --json` |
| `ufis-mem-bench` | Memory throughput benchmark at an address | `ufis-mem-bench 0x40000000` |
| `ufis-irq-stat` | Interrupt statistics monitor | `ufis-irq-stat --json` |
| `ufis-logic-monitor` | Track register bitfield transitions | `ufis-logic-monitor 0x43C10000 0xFF 0.2` |
| `ufis_status` | Branded system and FPGA quick status | `ufis_status` |

Full tool details: [`docs/UFIS_TOOLS_REFERENCE.md`](docs/UFIS_TOOLS_REFERENCE.md)

## Build

```bash
cd ufis_na_linux
petalinux-build
```

Typical generated artifacts are in `images/linux/`:

- `BOOT.BIN`
- `image.ub`
- `rootfs.cpio.gz.u-boot`
- `rootfs.ext4`
- `system.dtb`
- `system.bit`

Repository policy: generated `images/linux/*` build outputs are intentionally not versioned in Git.
The repository contains source/config/hardware handoff files needed to rebuild these artifacts locally.

## Bitstream upload endpoint

- Service: `ufis-bitstream-manager.service` (enabled by default)
- Listener: `0.0.0.0:5001`
- Upload behavior: receives bytes to `/tmp/received_bitstream.bit`, then calls `fpgautil -b /tmp/received_bitstream.bit`

## Network bootstrap behavior

- Service: `ufis-net-init.service` (enabled by default)
- Logic:
  - Detect first active non-loopback interface (for example `end0`)
  - Try DHCP (`udhcpc`)
  - If no DHCP lease is offered, apply fallback static IP `192.168.2.50/24`

Override options:

- `UFIS_NET_IF` to force interface name
- `UFIS_STATIC_IP` to change fallback CIDR (for example `192.168.2.60/24`)

## Notes

- The package name `nisl-achermann-branding` is kept for compatibility with current rootfs config.
- Custom layer compatibility is set to Yocto/PetaLinux series `scarthgap`.
