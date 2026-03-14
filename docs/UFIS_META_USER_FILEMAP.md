# UFIS `meta-user` File Map (Audited)

This is the full audited inventory of custom files in `project-spec/meta-user`.

## Layer configuration

| File | Role |
| --- | --- |
| `conf/layer.conf` | Registers layer, recipes, dynamic `meta-xilinx-tools` bbappends, and compatibility (`scarthgap`). |
| `conf/petalinuxbsp.conf` | PetaLinux BSP customization hook file (currently minimal). |
| `conf/user-rootfsconfig` | User package selections injected into rootfs menu. |
| `COPYING.MIT` | Layer license text. |
| `README` | Layer-specific documentation. |

## Applications (`recipes-apps`)

### `nisl-achermann-branding`

| File | Role |
| --- | --- |
| `recipes-apps/nisl-achermann-branding/nisl-achermann-branding.bb` | Recipe installing UFIS status/network bootstrap utilities and systemd service. |
| `recipes-apps/nisl-achermann-branding/files/ufis_status.sh` | Runtime status command (`/usr/bin/ufis_status`). |
| `recipes-apps/nisl-achermann-branding/files/ufis_net_init.sh` | Boot-time network bootstrap helper (`/usr/bin/ufis_net_init`) with DHCP then static fallback. |
| `recipes-apps/nisl-achermann-branding/files/ufis-net-init.service` | systemd unit enabling automatic network bootstrap at boot. |

### `ufis-bitstream-manager`

| File | Role |
| --- | --- |
| `recipes-apps/ufis-bitstream-manager/ufis-bitstream-manager.bb` | Recipe + systemd integration for bitstream server service. |
| `recipes-apps/ufis-bitstream-manager/files/ufis-bitstream-manager.service` | Auto-start service unit. |
| `recipes-apps/ufis-bitstream-manager/files/ufis_bitstream_server.py` | TCP server receiving `.bit` data and invoking `fpgautil -b`. |
| `recipes-apps/ufis-bitstream-manager/files/ufis_load_bit.sh` | Manual helper for local bitstream load. |

### `ufis-hw-tools`

| File | Role |
| --- | --- |
| `recipes-apps/ufis-hw-tools/ufis-hw-tools.bb` | Recipe installing UFIS diagnostic tools and Python runtime deps. |
| `recipes-apps/ufis-hw-tools/files/ufis_hw_scan.py` | Platform device scanner (`/sys/bus/platform/devices`). |
| `recipes-apps/ufis-hw-tools/files/ufis_reg.py` | Direct register read/write via `/dev/mem`. |
| `recipes-apps/ufis-hw-tools/files/ufis_health.py` | XADC + system-load health report. |
| `recipes-apps/ufis-hw-tools/files/ufis_mem_bench.py` | Memory read throughput benchmark. |
| `recipes-apps/ufis-hw-tools/files/ufis_irq_stat.py` | `/proc/interrupts` monitor and JSON export. |
| `recipes-apps/ufis-hw-tools/files/ufis_logic_monitor.py` | Register transition monitor (bit-level change detection). |

## Board support (`recipes-bsp`)

| File | Role |
| --- | --- |
| `recipes-bsp/device-tree/device-tree.bbappend` | Appends custom DT include and conditional SDT behavior. |
| `recipes-bsp/device-tree/device-tree-sdt.inc` | Shared include appending `system-user.dtsi`. |
| `recipes-bsp/device-tree/files/system-user.dtsi` | User DT include placeholder extending generated `system-conf.dtsi`. |
| `recipes-bsp/u-boot/u-boot-xlnx_%.bbappend` | U-Boot append adding `platform-top.h` and `bsp.cfg`. |
| `recipes-bsp/u-boot/files/bsp.cfg` | U-Boot config flags (config name, boot script offset). |
| `recipes-bsp/u-boot/files/platform-top.h` | Platform-specific U-Boot header aggregation. |

## Xilinx tools dynamic layer

| File | Role |
| --- | --- |
| `meta-xilinx-tools/recipes-bsp/uboot-device-tree/uboot-device-tree.bbappend` | Appends custom `system-user.dtsi` into u-boot device-tree flow. |
| `meta-xilinx-tools/recipes-bsp/uboot-device-tree/files/system-user.dtsi` | DT include placeholder for U-Boot DT path. |

## Kernel (`recipes-kernel`)

| File | Role |
| --- | --- |
| `recipes-kernel/linux/linux-xlnx_%.bbappend` | Appends kernel BSP config fragment. |
| `recipes-kernel/linux/linux-xlnx/bsp.cfg` | Kernel BSP config fragment file (currently empty placeholder). |

## Core overrides (`recipes-core`)

| File | Role |
| --- | --- |
| `recipes-core/base-files/base-files_%.bbappend` | Extends `base-files` to provide UFIS-branded MOTD. |
| `recipes-core/base-files/files/motd` | Login banner content installed as `/etc/motd`. |

## Packaging path summary

```mermaid
flowchart LR
    A[recipes-apps/*.bb] --> B[do_install]
    B --> C[/usr/bin UFIS tools]
    B --> E[systemd unit]
    E --> F[Boot-time bitstream service]
    G[recipes-core/base-files bbappend] --> D[/etc/motd]
```
