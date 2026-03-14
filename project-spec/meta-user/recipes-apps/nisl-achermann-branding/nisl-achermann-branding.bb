SUMMARY = "Custom branding and utilities for UFIS-NA Linux image"
SECTION = "PETALINUX/apps"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://ufis_status.sh \
           file://ufis_net_init.sh \
           file://ufis-net-init.service \
          "

S = "${WORKDIR}"

inherit systemd

SYSTEMD_PACKAGES = "${PN}"
SYSTEMD_SERVICE:${PN} = "ufis-net-init.service"
SYSTEMD_AUTO_ENABLE:${PN} = "enable"

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${WORKDIR}/ufis_status.sh ${D}${bindir}/ufis_status
    install -m 0755 ${WORKDIR}/ufis_net_init.sh ${D}${bindir}/ufis_net_init

    install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${WORKDIR}/ufis-net-init.service ${D}${systemd_system_unitdir}/ufis-net-init.service
}

FILES:${PN} += "${systemd_system_unitdir}/ufis-net-init.service"
