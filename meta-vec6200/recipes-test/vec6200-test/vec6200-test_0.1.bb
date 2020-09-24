DESCRIPTION = "vec6200 self test"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://vec6200-test.py"

RDEPENDS_${PN} = "python3-core python3-unittest"

# Add tpm2 test dependencies
RDEPENDS_${PN} += "ibmtpm20tss"

# Add accel and gyro dependencies
RDEPENDS_${PN} += "libiio-tests"

# Add status led dependencies
RDEPENDS_${PN} += "iointerface"

# Add rs232, rs485, can dependencies
RDEPENDS_${PN} += "canutils loopback-test"

do_install () {
    install -d ${D}${bindir}
    install -m 0755 ${WORKDIR}/vec6200-test.py ${D}${bindir}/vec6200-test
}
