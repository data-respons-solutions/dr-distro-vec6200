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
	alsa-utils-scripts \
	firmware-i210 \
	vec6200-test \
"

ROOTFS_POSTPROCESS_COMMAND_append = " add_mountpoints;"

add_mountpoints() {
	install -d ${IMAGE_ROOTFS}/opt
	install -d ${IMAGE_ROOTFS}/opt/app
	install -d ${IMAGE_ROOTFS}/opt/data
	echo "PARTLABEL=app      /opt/app        ext4       defaults,ro,nofail           0  0" >> ${IMAGE_ROOTFS}/etc/fstab
	echo "PARTLABEL=data     /opt/data       ext4       defaults,rw,nofail           0  0" >> ${IMAGE_ROOTFS}/etc/fstab
}
