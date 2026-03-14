SUMMARY = "Bitstream manager service for UFIS-NA"
SECTION = "PETALINUX/apps"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://ufis_bitstream_server.py \
           file://ufis-bitstream-manager.service \
           file://ufis_load_bit.sh \
          "

S = "${WORKDIR}"

inherit systemd

SYSTEMD_PACKAGES = "${PN}"
SYSTEMD_SERVICE:${PN} = "ufis-bitstream-manager.service"
SYSTEMD_AUTO_ENABLE:${PN} = "enable"

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${WORKDIR}/ufis_bitstream_server.py ${D}${bindir}/ufis_bitstream_server.py
    install -m 0755 ${WORKDIR}/ufis_load_bit.sh ${D}${bindir}/ufis_load_bit.sh
    
    install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${WORKDIR}/ufis-bitstream-manager.service ${D}${systemd_system_unitdir}/ufis-bitstream-manager.service
}

FILES:${PN} += "${systemd_system_unitdir}/ufis-bitstream-manager.service"
