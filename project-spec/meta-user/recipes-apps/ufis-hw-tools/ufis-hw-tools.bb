#
# Recipe for UFIS-NA Hardware Tools
#

SUMMARY = "Custom hardware diagnostic and management tools for UFIS-NA project"
SECTION = "PETALINUX/apps"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://ufis_hw_scan.py \
           file://ufis_reg.py \
           file://ufis_health.py \
           file://ufis_mem_bench.py \
           file://ufis_irq_stat.py \
           file://ufis_logic_monitor.py \
"

S = "${WORKDIR}"

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ufis_hw_scan.py ${D}${bindir}/ufis-hw-scan
    install -m 0755 ufis_reg.py ${D}${bindir}/ufis-reg
    install -m 0755 ufis_health.py ${D}${bindir}/ufis-health
    install -m 0755 ufis_mem_bench.py ${D}${bindir}/ufis-mem-bench
    install -m 0755 ufis_irq_stat.py ${D}${bindir}/ufis-irq-stat
    install -m 0755 ufis_logic_monitor.py ${D}${bindir}/ufis-logic-monitor
}

RDEPENDS:${PN} = "python3-core python3-json python3-mmap python3-io python3-datetime"
