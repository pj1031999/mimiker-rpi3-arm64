CURL = curl -L
RM = rm -f

ISL = isl-0.21
MPFR = mpfr-4.0.2
GMP = gmp-6.1.2
MPC = mpc-1.1.0
BINUTILS = binutils-2.32
GCC = gcc-8.3.0
GDB = gdb-8.2.1

ROOTDIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
HOSTDIR := $(ROOTDIR)/host
PREFIX ?= $(ROOTDIR)/local
TARGET = aarch64-rpi3-elf

all: gcc-install gdb-install

clean: gmp-clean mpfr-clean mpc-clean isl-clean binutils-clean gcc-clean
	$(RM) -r host
	$(RM) *~

### The GNU Multiple Precision Arithmetic Library

$(GMP).tar.xz:
	$(CURL) -o $@ "https://gmplib.org/download/gmp/$(GMP).tar.xz"

gmp-unpack: $(GMP)/.unpack
$(GMP)/.unpack: $(GMP).tar.xz
	tar xvJf $^
	touch $@

gmp-configure: $(GMP)/.configure
$(GMP)/.configure: $(GMP)/.unpack
	cd $(GMP) && ./configure \
		--disable-shared --prefix=$(HOSTDIR)
	touch $@

gmp-build: $(GMP)/.build
$(GMP)/.build: $(GMP)/.configure
	cd $(GMP) && $(MAKE)
	touch $@

gmp-install: $(GMP)/.install
$(GMP)/.install: $(GMP)/.build
	cd $(GMP) && $(MAKE) install
	touch $@

gmp-clean:
	$(RM) -r $(GMP)

.PHONY: gmp-unpack gmp-configure gmp-build gmp-install gmp-clean

### Library for multiple-precision floating-point computations

$(MPFR).tar.xz:
	$(CURL) -o $@ "https://www.mpfr.org/mpfr-current/$(MPFR).tar.xz"

mpfr-unpack: $(MPFR)/.unpack
$(MPFR)/.unpack: $(MPFR).tar.xz
	tar xvJf $^
	touch $@

mpfr-configure: $(MPFR)/.configure
$(MPFR)/.configure: $(MPFR)/.unpack
	cd $(MPFR) && ./configure \
		--disable-shared --prefix=$(HOSTDIR) --with-gmp=$(HOSTDIR)
	touch $@

mpfr-build: $(MPFR)/.build
$(MPFR)/.build: $(MPFR)/.configure
	cd $(MPFR) && $(MAKE)
	touch $@

mpfr-install: $(MPFR)/.install
$(MPFR)/.install: $(MPFR)/.build
	cd $(MPFR) && $(MAKE) install
	touch $@

mpfr-clean:
	$(RM) -r $(MPFR)

.PHONY: mpfr-unpack mpfr-configure mpfr-build mpfr-install mpfr-clean

### Library for the arithmetic of complex numbers

$(MPC).tar.gz:
	$(CURL) -o $@ "https://ftp.gnu.org/gnu/mpc/$(MPC).tar.gz"

mpc-unpack: $(MPC)/.unpack
$(MPC)/.unpack: $(MPC).tar.gz
	tar xvzf $^
	touch $@

mpc-configure: $(MPC)/.configure
$(MPC)/.configure: $(MPC)/.unpack $(GMP)/.install $(MPFR)/.install
	cd $(MPC) && ./configure \
		--disable-shared \
		--prefix=$(HOSTDIR) \
		--with-gmp=$(HOSTDIR) \
		--with-mpfr=$(HOSTDIR)
	touch $@

mpc-build: $(MPC)/.build
$(MPC)/.build: $(MPC)/.configure
	cd $(MPC) && $(MAKE)
	touch $@

mpc-install: $(MPC)/.install
$(MPC)/.install: $(MPC)/.build
	cd $(MPC) && $(MAKE) install
	touch $@

mpc-clean:
	$(RM) -r $(MPC)

.PHONY: mpc-unpack mpc-configure mpc-build mpc-install mpc-clean

### Integer Set Library

$(ISL).tar.xz:
	$(CURL) -o $@ "http://isl.gforge.inria.fr/$(ISL).tar.xz"

isl-unpack: $(ISL)/.unpack
$(ISL)/.unpack: $(ISL).tar.xz
	tar xvJf $^
	touch $@

isl-configure: $(ISL)/.configure
$(ISL)/.configure: $(ISL)/.unpack $(GMP)/.install
	cd $(ISL) && ./configure \
		--disable-shared \
		--prefix=$(HOSTDIR) \
		--with-gmp-prefix=$(HOSTDIR)
	touch $@

isl-build: $(ISL)/.build
$(ISL)/.build: $(ISL)/.configure
	cd $(ISL) && $(MAKE)
	touch $@

isl-install: $(ISL)/.install
$(ISL)/.install: $(ISL)/.build
	cd $(ISL) && $(MAKE) install
	touch $@

isl-clean:
	$(RM) -r $(ISL)

.PHONY: isl-unpack isl-configure isl-build isl-install isl-clean

### GNU Binutils

$(BINUTILS).tar.xz:
	$(CURL) -o $@ "https://ftp.gnu.org/gnu/binutils/$(BINUTILS).tar.xz"

binutils-unpack: $(BINUTILS)/.unpack
$(BINUTILS)/.unpack: $(BINUTILS).tar.xz
	tar xvJf $^
	touch $@

binutils-configure: $(BINUTILS)/.configure
$(BINUTILS)/.configure: $(BINUTILS)/.unpack $(ISL)/.install $(MPC)/.install
	cd $(BINUTILS) && ./configure \
		--target=$(TARGET) \
		--disable-nls \
		--prefix=$(PREFIX) \
		--with-gmp=$(HOSTDIR) \
		--with-mpfr=$(HOSTDIR) \
		--with-mpc=$(HOSTDIR) \
		--with-isl=$(HOSTDIR)
	touch $@

binutils-build: $(BINUTILS)/.build
$(BINUTILS)/.build: $(BINUTILS)/.configure
	cd $(BINUTILS) && $(MAKE)
	touch $@

binutils-install: $(BINUTILS)/.install
$(BINUTILS)/.install: $(BINUTILS)/.build
	cd $(BINUTILS) && $(MAKE) install
	touch $@

binutils-clean:
	$(RM) -r $(BINUTILS)

.PHONY: binutils-unpack binutils-configure binutils-build binutils-install binutils-clean

### GNU Compiler Collection

$(GCC).tar.xz:
	$(CURL) -o $@ "https://ftp.gnu.org/gnu/gcc/$(GCC)/$(GCC).tar.xz"

gcc-unpack: $(GCC)/.unpack
$(GCC)/.unpack: $(GCC).tar.xz
	tar xvJf $^
	touch $@

gcc-configure: $(GCC)/.configure
$(GCC)/.configure: $(GCC)/.unpack $(BINUTILS)/.install
	rm -rf $(GCC)-build &&	mkdir $(GCC)-build
	cd $(GCC)-build && PATH=$(PREFIX)/bin:$$PATH\
	 ./../$(GCC)/configure \
  	--target=$(TARGET) \
	  --prefix=$(PREFIX) \
  	--datarootdir=$(PREFIX)/$(TARGET)/share \
	  --with-mpc=$(HOSTDIR) \
	  --with-gmp=$(HOSTDIR) \
	  --with-mpfr=$(HOSTDIR) \
	  --with-isl=$(HOSTDIR) \
	  --enable-lto \
	  --enable-languages=c \
	  --disable-multilib \
	  --disable-nls \
	  --disable-shared \
	  --disable-werror \
	  --with-newlib \
	  --without-headers \
    --with-arch=armv8-a \
    --with-cpu=cortex-a53
	touch $@

gcc-build: $(GCC)/.build
$(GCC)/.build: $(GCC)/.configure
	cd $(GCC)-build && $(MAKE) all-gcc
	cd $(GCC)-build && $(MAKE) all-target-libgcc
	touch $@

gcc-install: $(GCC)/.install
$(GCC)/.install: $(GCC)/.build
	cd $(GCC)-build && $(MAKE) install-gcc
	cd $(GCC)-build && $(MAKE) install-target-libgcc
	touch $@

gcc-clean:
	$(RM) -r $(GCC)

.PHONY: gcc-unpack gcc-configure gcc-build gcc-install gcc-clean

### GNU Debugger

$(GDB).tar.xz:
	$(CURL) -o $@ "https://ftp.gnu.org/gnu/gdb/$(GDB).tar.xz"

gdb-unpack: $(GDB)/.unpack
$(GDB)/.unpack: $(GDB).tar.xz
	tar xvJf $^
	touch $@

gdb-configure: $(GDB)/.configure
$(GDB)/.configure: $(GDB)/.unpack $(ISL)/.install
	cd $(GDB) && PATH=$(PREFIX)/bin:$$PATH ./configure \
		--target=$(TARGET)\
		--with-isl=$(HOSTDIR) \
		--prefix=$(PREFIX) \
	  --datarootdir=$(PREFIX)/$(TARGET)/share \
    --with-sysroot=$(PREFIX)/$(TARGET) \
    --disable-binutils \
    --disable-gas \
    --disable-ld \
    --disable-nls \
		--disable-sim \
		--disable-werror \
		--with-tui \
		--with-python=$(shell which python3)
	touch $@

gdb-build: $(GDB)/.build
$(GDB)/.build: $(GDB)/.configure
	cd $(GDB) && $(MAKE)
	touch $@

gdb-install: $(GDB)/.install
$(GDB)/.install: $(GDB)/.build
	cd $(GDB) && $(MAKE) install
	touch $@

gdb-clean:
	$(RM) -r $(GDB)

.PHONY: gdb-unpack gdb-configure gdb-build gdb-install gdb-clean
