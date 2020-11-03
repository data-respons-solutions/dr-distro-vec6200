DESCRIPTION = "vec6200 service image"

require vec6200-image.bb

IMAGE_INSTALL_append += " \
	flash-fuse \
	loopback-test \
	firmware-i210 \
	vec6200-test \
	iperf3 \
"
