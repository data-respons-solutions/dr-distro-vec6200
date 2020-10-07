VEC6200 SDK
===========

## Maintainer
Mikko Salomäki <ms@datarespons.se>

## Build
External recipe sources are included in the project as git submodules.
These modules need to be initialized on first use:

Start of by initializing git

`$ git submodule update --init`

OpenEmbedded (BitBake) relies on the build environment providing a large
set of environment variables.  These are most easily set up by sourcing
the provide 'env' script:

`$ . ./env`

This will generate artifacts under the build sub-folder.
Read freescale EULA at:

`<top of project>/meta-freescale/EULA`

If you accept, set ACCEPT\_FSL\_EULA from "0" to "1" in your newly generated local.conf:

`<top of project>/build/conf/local.conf`


If you need more flexibility in where to build do:

```
$ export TEMPLATECONF=<top of project>/build/conf
$ export DR_CM_COMMIT=`git -C <top of project> describe --tags --long --dirty`
$ export DR_BUILD_PLAN=<name of your build>
$ export DR_BUILD_NO=<yout build number if needed>
$ export BB_ENV_EXTRAWHITE="DR_BUILD_PLAN DR_BUILD_NO DR_CM_COMMIT"
$ source <top of project>/oe-core/oe-init-build-env build <top of project>/bitbake/
```

### Factory
Needed for flashing u-boot through SDP (serial download protocol).
Generate factory image , factory tools and u-boot(factory and production) binaries:

```
$ bitbake factory-tools
$ MACHINE=vec6200-factory bitbake factory-image
```

### Datarespons reference distro
`$ bitbake vec6200-image`

### Datarespons reference distro SDK
`$ bitbake vec6200-image -c populate_sdk`


## Usage

### Console
Serial console through debug card, baud 115200.

ssh by certificate. Reference distro certificate in meta-datarespons/recipes-security/ssh-keys/droot

`$ ssh -i droot root@ip`

### Applications
**swap-root**

Update rootfs
 
**image-install**

Fresh install from USB

**dioctl**

Example application for accesing digital inputs and outputs

**anctl**

Example application for accessing analog inputs

**status-led**

Example application for setting status led

### Interfaces
**serial**

Linux char devices:

/dev/ttymxc0: console

/dev/ttymxc1: COM1 (+rtscts)

/dev/ttymxc2: gpsd reserved

/dev/ttymxc3: COM2 (+rtscts)

/dev/ttymxc4: bluetooth (optional m.2)

/dev/ttySMC: smc reserved

/dev/ttyVEC0: RS485_A
* Termination: /sys/class/gpio/gpio489/value
* J1708: /sys/class/gpio/gpio488/value

/dev/ttyVEC1: RS485_B
* Termination: /sys/class/gpio/gpio485/value
* J1708: /sys/class/gpio/gpio484/value

**can**

Transceiver default mode is listen only. Set transceiver gpio to 1 to enable

Linux socket devices:

can0:
* Termination: /sys/class/gpio/gpio95/value
* Transceiver: /sys/class/gpio/gpio508/value

can1:
* Termination: /sys/class/gpio/gpio9/value
* Transceiver: /sys/class/gpio/gpio509/value

**gps**

gps connected to gpsd.

**tpm2.0**

Linux char device.

**accelerometer**

iio_device: lsm6dsm_accel

Access through libiio

**gyro**

iio device: lsm6dsm_gyro

Access through libiio

**audio**

ALSA sound card: vec6200_audio1


### Flash u-boot
* Build tools and binaries: [Factory](#Factory)
* Install factory tools:

`$ <top of project>/build/tmp-glibc/deploy/sdk/vec6200-factory-tools-*.sh`

* Source tools environment:

`$ . <tools install dir>/environment-setup-*`

* Set system into [Rescue mode](#Rescue%20mode).
* Extract and run factory image (Connect to system console for progress)

```
$ cd <top of project>/build/tmp-glibc/deploy/images/vec6200-factory
$ sudo imx_usb -c .
```

### Rescue mode
Forcing system into rescue mode allows re-flashing u-boot externally with factory image.
Connect debug board and set jumper JP6 to 1-2.
