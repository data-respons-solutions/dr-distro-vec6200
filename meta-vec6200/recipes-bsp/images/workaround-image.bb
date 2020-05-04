DESCRIPTION = "Container image with artifacts required for booting system with rev A"
LICENSE = "MIT"

INITRD_IMAGE = "datarespons-image-initramfs"

FACTORY_IMAGE_INSTALL ?= ""
IMAGE_INSTALL += "\
	kernel-image \
	devicetree \
	u-boot \
"
IMAGE_CONTAINER_NO_DUMMY = "1"
IMAGE_FSTYPES = "container"
IMAGE_LINGUAS = ""
#IMAGE_PREPROCESS_COMMAND_remove = " prelink_setup; prelink_image; mklibs_optimize_image;"

do_initrd[depends] += " \
	${INITRD_IMAGE}:do_image_complete \
"

addtask do_initrd after do_rootfs before do_image

do_initrd () {
	install -d ${IMAGE_ROOTFS}/boot
	install -m 0644 ${DEPLOY_DIR_IMAGE}/${INITRD_IMAGE}-${MACHINE}.${INITRAMFS_FSTYPES} ${IMAGE_ROOTFS}/boot/
}

inherit core-image dr-image-info
