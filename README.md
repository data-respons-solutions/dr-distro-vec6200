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
`$ bitbake datarespons-image`

### Datarespons reference distro SDK
`$ bitbake datarespons-image -c populate_sdk`


## Usage
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
$ tar -xf factory-image-vec6200-factory.tar.bz
$ cd boot
$ sudo imx_usb -c .
```

### Rescue mode
Forcing system into rescue mode allows re-flashing u-boot externally with factory image.
Connect debug board and set jumper X.
