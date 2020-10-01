DESCRIPTION = "vec6200 service image initramfs"

require vec6200-service-image.bb

IMAGE_FSTYPES = "${INITRAMFS_FSTYPES}"

ROOTFS_POSTPROCESS_COMMAND_append = " remove_kernel_image;"

remove_kernel_image() {
	rm ${IMAGE_ROOTFS}/boot/${KERNEL_IMAGETYPE}*
}
