DESCRIPTION = "vec6200 reference image"

require recipes-bsp/images/datarespons-image.bb

IMAGE_INSTALL_append += " \
	flash-fuse \
	intel-eeprom-access-tool \
	loopback-test \
	image-install \
	swap-root \
	iointerface \
	canutils \
"