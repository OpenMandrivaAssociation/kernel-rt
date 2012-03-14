# -*- Mode: rpm-spec -*-
#
# (c) Mandriva
#
# The kernel-2.6-linus package (and so this spec file) is under development,
# it does mean:
#
#    1. You can have nasty surprises when playing with the package
#    generation
#
#    2. Is easier to go and come back from Mordor than adding a new
#    architecture support
#
#    3. A known architecture with just a missing .config shouldn't be too
#    hard, but as this spec changes too fast, it's likely to be broken
# 
#
# if you try to understand kernel numbering, read docs/kernel_naming

%define kernelversion	3
%define patchlevel	2

# kernel Makefile extraversion is substituted by 
# kpatch/kstable wich are either 0 (empty), rc (kpatch) or stable release (kstable)
%define kpatch		0
%define kstable		11

%define ktag		rt

# AKPM's release
%define rt_rel		20

# this is the releaseversion
%define mdvrelease 	1

# This is only to make life easier for people that creates derivated kernels
# a.k.a name it kernel-tmb :)
%define kname 		kernel-%{ktag}

%define rpmtag		%distsuffix
%if %kpatch
%define rpmrel		%mkrel 0.%{kpatch}.%{ktag}%{rt_rel}.%{mdvrelease}
%else
%define rpmrel		%mkrel 1.%{ktag}%{rt_rel}.%{mdvrelease}
%endif

# When we are using a pre/rc patch, the tarball is a patchlevel -1
%if %kpatch
%define kversion  	%{kernelversion}.%{patchlevel}.%{kstable}
%define tar_ver	  	%{kernelversion}.%(expr %{patchlevel} - 1)
%define rtversion	%{kernelversion}.%{patchlevel}-rc%{kpatch}-%{ktag}%{rt_rel}
%else
%if %kstable
%define kversion  	%{kernelversion}.%{patchlevel}.%{kstable}
%define rtversion	%{kversion}-%{ktag}%{rt_rel}
%define tar_ver   	%{kernelversion}.%{patchlevel}
%else
%define kversion  	%{kernelversion}.%{patchlevel}
%define rtversion	%{kernelversion}.%{patchlevel}-%{ktag}%{rt_rel}
%define tar_ver   	%{kernelversion}.%{patchlevel}
%endif
%endif
%define kverrel   	%{kversion}-%{rpmrel}

# used for not making too long names for rpms or search paths
%if %kpatch
%define buildrpmrel     0.%{kpatch}.%{ktag}%{rt_rel}.%{mdvrelease}%{rpmtag}
%else
%define buildrpmrel     1.%{ktag}%{rt_rel}.%{mdvrelease}%{rpmtag}
%endif

%define buildrel        %{kversion}-%{buildrpmrel}

%define rt_info NOTE: This kernel has no Mandriva patches and no third-party drivers, \
only Ingo Molnar -rt (realtime) series patches applied to vanille kernel.org \
kernels.

# having different top level names for packges means that you have to remove them by hard :(
%define top_dir_name    %{kname}-%{_arch}

%define build_dir       %{_builddir}/%{top_dir_name}
%define src_dir         %{build_dir}/linux-%{tar_ver}

# disable useless debug rpms...
%define _enable_debug_packages  %{nil}
%define debug_package           %{nil}

# build defines
%define build_doc 0
%define build_source 1
%define build_devel 1
%define build_debug 1

%define build_kernel 1

%define distro_branch %(perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?/; $_="$1.$2"' /etc/mandriva-release)

# End of user definitions
%{?_without_kernel: %global build_kernel 0}
%{?_without_doc: %global build_doc 0}
%{?_without_source: %global build_source 0}
%{?_without_devel: %global build_devel 0}

%{?_with_kernel: %global build_kernel 1}
%{?_with_doc: %global build_doc 1}
%{?_with_source: %global build_source 1}
%{?_with_devel: %global build_devel 1}


%if %(if [ -z "$CC" ] ; then echo 0; else echo 1; fi)
%define kmake %make CC="$CC"
%else
%define kmake %make 
%endif
# there are places where parallel make don't work
%define smake make

# Aliases for amd64 builds (better make source links?)
%define target_cpu	%(echo %{_target_cpu} | sed -e "s/amd64/x86_64/")
%define target_arch	%(echo %{_arch} | sed -e "s/amd64/x86_64/" -e "s/i386/x86/" -e "s/x86_64/x86/")


# Defines for the things that are needed for all the kernels
%define requires1 module-init-tools >= 3.0-%mkrel 7
%define requires2 mkinitrd >= 3.4.43-%mkrel 10
%define requires3 bootloader-utils >= 1.9
%define requires4 sysfsutils
%define requires5 kernel-firmware >= 2.6.27-0.rc2.2mdv

%define kprovides kernel = %{tar_ver}, alsa

# src.rpm description
Name:           %{kname}
Version:        %{kversion}
Release:        %{rpmrel}
License: 	GPLv2
Group: 		Development/Kernel
ExclusiveArch: 	%{ix86} x86_64
URL: 		http://www.kernel.org/
Summary:  The Linux Kernel
Provides: %kprovides
Requires: %requires1
Requires: %requires2
Requires: %requires3
Requires: %requires4
Requires: %requires5

####################################################################
#
# Sources
#
### This is for full SRC RPM
Source0:        ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.xz
Source1:        ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.sign
# This is for disabling mrproper on -devel rpms
Source2:	disable-mrproper-in-devel-rpms.patch
# This disables removal of bounds.h and asm-offsets.h in -devel rpms (from kernel-linus)
#SOURCE3:	kbuild-really-dont-remove-bounds-asm-offsets-headers.patch

Source4:  README.kernel-sources
Source5:  README.MandrivaLinux

Source20: i386.config
Source21: x86_64.config


####################################################################
#
# Patches

#
# Patch0 to Patch100 are for core kernel upgrades.
#

# Pre linus patch: ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing

%if %kpatch
Patch1:         ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing/patch-%{kernelversion}.%{patchlevel}-%{kpatch}.xz
Source10:       ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing/patch-%{kernelversion}.%{patchlevel}-%{kpatch}.sign
%endif
%if %kstable
Patch1:         ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/patch-%{kversion}.xz
Source10:       ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/patch-%{kversion}.sign
%endif

# Mingos patches
%if %kpatch
Patch2:		http://www.kernel.org/pub/linux/kernel/projects/rt/%{kernelversion}.%{patchlevel}/patch-%{rtersion}.patch.xz
Source11:	http://www.kernel.org/pub/linux/kernel/projects/rt/%{kernelversion}.%{patchlevel}/patch-%{rtversion}.patch.sign
%else
Patch2:		http://www.kernel.org/pub/linux/kernel/projects/rt/%{kernelversion}.%{patchlevel}/patch-%{rtversion}.patch.xz
Source11:	http://www.kernel.org/pub/linux/kernel/projects/rt/%{kernelversion}.%{patchlevel}/patch-%{rtversion}.patch.sign
%endif

# LKML's patches
#Patch102:	gpu-drm-nouveau-git-20100316.patch 
#Patch103:	gpu-drm-nouveau-fix-missing-locking.patch

# MDV Patches
#Patch201:	video-fb-fix-unregister_framebuffer-fb_destroy.patch

#END
####################################################################


Conflicts: drakxtools-backend < 10.4.140
Autoreqprov: 	no
BuildRequires: 	gcc module-init-tools >= 0.9.15

%description
%{rt_info}


#
# kernel-source: kernel sources
#
%if %build_source
%package -n %{kname}-source
Version:  %{kversion}
Release:  %{rpmrel}
Provides: kernel-source = %{kverrel}, kernel-devel = %{kverrel}
Requires: glibc-devel, ncurses-devel, make, gcc, perl
Summary:  The source code for the Linux kernel
Group:    Development/Kernel
Autoreqprov: no

%description -n %{kname}-source
The %{kname}-source package contains the source code files for the Linux 
kernel. Theese source files are only needed if you want to build your own 
custom kernel that is better tuned to your particular hardware.

If you only want the files needed to build 3rdparty (nVidia, Ati, dkms-*,...)
drivers against, install the *-devel-* rpm that is matching your kernel.

%{rt_info}
%endif # build_source


# 
# kernel-devel: stripped kernel sources
#
%if %build_devel
%package -n %{kname}-devel
Version:  %{kversion}
Release:  %{rpmrel}
Provides: kernel-devel = %{kverrel}
Summary:  The %{kname} devel files for 3rdparty modules build
Group:    Development/Kernel
Autoreqprov: no
Requires: glibc-devel, ncurses-devel, make, gcc, perl

%description -n %{kname}-devel
This package contains the kernel-devel files that should be enough to build 
3rdparty drivers against for use with the %{kname}.

If you want to build your own kernel, you need to install the full 
%{kname}-source rpm.

%{rt_info}
%endif # build_devel

# 
# kernel-debug: unstripped kernel vmlinux
#
%if %build_debug
%package -n %{kname}-debuginfo
Version:  %{kversion}
Release:  %{rpmrel}
Provides: kernel-debug = %{kverrel}
Provides: kernel-debuginfo = %{kverrel}
Summary:  The %{kname} debug files
Group:    Development/Debug
Autoreqprov: no
Requires: glibc-devel

%description -n %{kname}-debuginfo
This package contains the kernel-debug files that should be enough to 
use debugging/monitoring tool (like systemtap, oprofile, ...)

%{rt_info}
%endif # build_debug

#
# kernel-doc: documentation for the Linux kernel
#
%if %build_doc
%package -n %{kname}-doc
Version:  %{kversion}
Release:  %{rpmrel}
Summary:  Various documentation bits found in the kernel source
Group:    Books/Computer books

%description -n %{kname}-doc
This package contains documentation files form the kernel source. Various
bits of information about the Linux kernel and the device drivers shipped
with it are documented in these files. You also might want install this
package if you need a reference to the options that can be passed to Linux
kernel modules at load time.

%{rt_info}
%endif # build_doc

#
# End packages - here begins build stage
#
%prep
%setup -q -n %top_dir_name -c

pushd %src_dir
%if %kpatch
xzcat %{PATCH1} | patch -p1
%endif
%if %kstable
xzcat %{PATCH1} | patch -p1
#patch1 -p1
%endif

# Mingo's patch
xzcat %{PATCH2} | patch -p1
#patch2 -p1

# LKML's patches
#patch102 -p1
#patch103 -p1

# MDV Patches
#patch201 -p1

popd

# PATCH END


#
# Setup Begin
#

# Copy our defconfigs into place.
%if %{_arch} == i386
cp %{SOURCE20} %{build_dir}/linux-%{tar_ver}/arch/%{target_arch}/defconfig
%else
%if %{_arch} == x86_64
cp %{SOURCE21} %{build_dir}/linux-%{tar_ver}/arch/%{target_arch}/defconfig
%endif
%endif

# make sure the kernel has the sublevel we know it has...
#LC_ALL=C perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{sublevel}/" linux-%{tar_ver}/Makefile

# remove localversion-tip file
rm -f linux-%{tar_ver}/localversion-rt

%build
# Common target directories
%define _kerneldir /usr/src/%{kname}-%{buildrel}
%define _bootdir /boot
%define _modulesdir /lib/modules
%define _develdir /usr/src/%{kname}-devel-%{buildrel}


# Directories definition needed for building
%define temp_root %{build_dir}/temp-root
%define temp_source %{temp_root}%{_kerneldir}
%define temp_boot %{temp_root}%{_bootdir}
%define temp_modules %{temp_root}%{_modulesdir}
%define temp_devel %{temp_root}%{_develdir}


PrepareKernel() {
	name=$1
	extension=$2
	echo "Prepare compilation of kernel $extension"

	if [ "$name" ]; then
		config_name="defconfig-$name"
	else
		config_name="defconfig"
	fi

	# make sure EXTRAVERSION says what we want it to say
#	%%if %kstable
#		LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = .%{kstable}-$extension/" Makefile
#	%%else
		LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -$extension/" Makefile
#	%%endif
	
	### FIXME MDV bugs #29744, #29074, will be removed when fixed upstream
	LC_ALL=C perl -p -i -e "s/^source/### source/" drivers/crypto/Kconfig
	
	%smake -s mrproper
	cp arch/%{target_arch}/$config_name .config
	%smake oldconfig
}


BuildKernel() {
	KernelVer=$1
	echo "Building kernel $KernelVer"

	%kmake all

	## Start installing stuff
	install -d %{temp_boot}
	install -m 644 System.map %{temp_boot}/System.map-$KernelVer
	install -m 644 .config %{temp_boot}/config-$KernelVer

	cp -f arch/%{target_arch}/boot/bzImage %{temp_boot}/vmlinuz-$KernelVer
	cp -f vmlinux %{temp_boot}/vmlinux-$KernelVer

	# modules
	install -d %{temp_modules}/$KernelVer
	%smake INSTALL_MOD_PATH=%{temp_root} KERNELRELEASE=$KernelVer modules_install 

	# remove /lib/firmware, we use a separate kernel-firmware
	rm -rf %{temp_root}/lib/firmware
}


SaveDevel() {
	flavour=$1
	if [ "$flavour" = "up" ]; then
		DevelRoot=%{temp_devel}
	else
		DevelRoot=%{temp_smp_devel}
	fi
	mkdir -p $DevelRoot
	for i in $(find . -name 'Makefile*'); do cp -R --parents $i $DevelRoot;done
	for i in $(find . -name 'Kconfig*' -o -name 'Kbuild*'); do cp -R --parents $i $DevelRoot;done
	cp -fR include $DevelRoot
	cp -fR scripts $DevelRoot
	%ifarch %{ix86} x86_64
		cp -fR arch/x86/kernel/asm-offsets.{c,s} $DevelRoot/arch/x86/kernel/
		cp -fR arch/x86/kernel/asm-offsets_{32,64}.c $DevelRoot/arch/x86/kernel/
		cp -fR arch/x86/include $DevelRoot/arch/x86/
	%else
		cp -fR arch/%{target_arch}/kernel/asm-offsets.{c,s} $DevelRoot/arch/%{target_arch}/kernel/
		cp -fR arch/%{target_arch}/include $DevelRoot/arch/%{target_arch}/
	%endif
	cp -fR .config Module.symvers $DevelRoot

        # Needed for truecrypt build (Danny)
	cp -fR drivers/md/dm.h $DevelRoot/drivers/md/

	# Needed for external dvb tree (#41418)
	cp -fR drivers/media/dvb/dvb-core/*.h %{temp_devel}/drivers/media/dvb/dvb-core/
	cp -fR drivers/media/dvb/frontends/lgdt330x.h %{temp_devel}/drivers/media/dvb/frontends/

	# add acpica header files, needed for fglrx build
	cp -fR drivers/acpi/acpica/*.h %{temp_devel}/drivers/acpi/acpica/

	# Disable bounds.h and asm-offsets.h removal
	#patch -p1 -d %{temp_devel} -i %{SOURCE3}

	# fix permissions
	chmod -R a+rX $DevelRoot
}

SaveDebug() {
	kernversion=$1
	flavour=$2

	echo "SaveDebug $kernversion $flavour"

	kernel_debug_files=../kernel_debug_files.$flavour

	echo "%defattr(-,root,root)" > $kernel_debug_files
	echo "%{_bootdir}/vmlinux-$kernversion" >> $kernel_debug_files

	find %{temp_modules}/$kernversion/kernel \
		-name "*.ko" -exec objcopy --only-keep-debug '{}' '{}'.debug \;

	find %{temp_modules}/$kernversion/kernel \
		-name "*.ko" -exec objcopy --add-gnu-debuglink='{}'.debug --strip-debug '{}' \;

	pushd %{temp_modules}
	find $kernversion/kernel -name "*.ko.debug" > debug_module_list
	popd

	cat %{temp_modules}/debug_module_list | sed 's|\(.*\)|%{_modulesdir}/\1|' >> $kernel_debug_files
	cat %{temp_modules}/debug_module_list | sed 's|\(.*\)|%exclude %{_modulesdir}/\1|' >> ../kernel_exclude_debug_files.$flavour
	rm -f %{temp_modules}/debug_module_list
}


CreateFiles() {
	kernversion=$1
	flavour=$2

	echo "CreateFiles $kernversion $flavour"

	output=../kernel_files.$kernversion

	echo "%defattr(-,root,root)" > $output
	echo "%{_bootdir}/config-${kernversion}" >> $output
	echo "%{_bootdir}/vmlinuz-${kernversion}" >> $output
	echo "%{_bootdir}/System.map-${kernversion}" >> $output
	echo "%dir %{_modulesdir}/${kernversion}/" >> $output
	echo "%{_modulesdir}/${kernversion}/kernel" >> $output
	echo "%{_modulesdir}/${kernversion}/modules.*" >> $output
	echo "%doc README.kernel-sources" >> $output
	echo "%doc README.MandrivaLinux" >> $output
	cat ../kernel_exclude_debug_files.$flavour >> $output
}


CreateKernel() {
	flavour=$1
	echo "CreateKernel $flavour"

	if [ "$flavour" = "up" ]; then
		KernelVer=%{buildrel}
		PrepareKernel "" %{buildrpmrel}
	else
		KernelVer=%{buildrel}$flavour
		PrepareKernel $flavour %{buildrpmrel}$flavour
	fi

	BuildKernel $KernelVer
	%if %build_devel
	    SaveDevel $flavour
	%endif
	%if %build_debug
	    SaveDebug $KernelVer $flavour
	%endif
        CreateFiles $KernelVer $flavour
}


###
# DO it...
###


# Create a simulacro of buildroot
rm -rf %{temp_root}
install -d %{temp_root}


#make sure we are in the directory
cd %src_dir

%if %build_kernel
CreateKernel up
%endif


# We don't make to repeat the depend code at the install phase
%if %build_source
PrepareKernel "" %{buildrpmrel}custom
# From > 2.6.13 prepare-all is deprecated and relies on include/linux/autoconf
# To have modpost and others scripts, one has to use the target scripts
%smake -s prepare
%smake -s scripts
%endif


###
### install
###
%install

# on ne strippe pas vmlinux
EXCLUDE_FROM_STRIP="%{_bootdir}/vmlinux"
export EXCLUDE_FROM_STRIP

install -m 644 %{SOURCE4}  .
install -m 644 %{SOURCE5}  .

cd %src_dir
# Directories definition needed for installing
%define target_source %{buildroot}/%{_kerneldir}
%define target_boot %{buildroot}%{_bootdir}
%define target_modules %{buildroot}%{_modulesdir}
%define target_devel %{buildroot}%{_develdir}

# We want to be able to test several times the install part
rm -rf %{buildroot}
cp -a %{temp_root} %{buildroot}

# Create directories infastructure
%if %build_source
install -d %{target_source} 

tar cf - . | tar xf - -C %{target_source}
chmod -R a+rX %{target_source}


# we remove all the source files that we don't ship

# first architecture files
for i in alpha arm arm26 avr32 blackfin cris frv h8300 hexagon ia64 mips microblaze m32r m68k m68knommu mn10300 openrisc parisc powerpc ppc score sh sh64 s390 sparc64 tile unicore32 v850 xtensa; do
	rm -rf %{target_source}/arch/$i
	rm -rf %{target_source}/include/asm-$i

%if %build_devel
%if %build_kernel
	rm -rf %{target_devel}/arch/$i
	rm -rf %{target_devel}/include/asm-$i
%endif # build_kernel
# Needed for truecrypt build (Danny)
%if %build_kernel
	cp -fR drivers/md/dm.h %{target_devel}/drivers/md/
%endif # build_kernel
%endif # build_devel
done

# remove arch files based on target arch
	rm -rf %{target_source}/arch/sparc
	rm -rf %{target_source}/arch/sparc64
	rm -rf %{target_source}/include/asm-sparc
	rm -rf %{target_source}/include/asm-sparc64
%if %build_devel
%if %build_kernel
	rm -rf %{target_devel}/arch/sparc
	rm -rf %{target_devel}/arch/sparc64
	rm -rf %{target_devel}/include/asm-sparc
	rm -rf %{target_devel}/include/asm-sparc64
%endif # build_kernel
%endif # build_devel

# other misc files
rm -f %{target_source}/{.config.old,.config.cmd,.tmp_gas_check,.mailmap,.missing-syscalls.d,.mm,arch/.gitignore}

# disable mrproper in -devel rpms
%if %build_devel
%if %build_kernel
patch -p1 -d %{target_devel} -i %{SOURCE2}
%endif # build_kernel
%endif # build_devel

%endif # build_source

# gzipping modules
find %{target_modules} -name "*.ko" | xargs gzip -9

# We used to have a copy of PrepareKernel here
# Now, we make sure that the thing in the linux dir is what we want it to be

for i in %{target_modules}/*; do
  rm -f $i/build $i/source $i/modules.*
done

# sniff, if we gzipped all the modules, we change the stamp :(
# we really need the depmod -ae here

pushd %{target_modules}
for i in *; do
	/sbin/depmod -u -ae -b %{buildroot} -r -F %{target_boot}/System.map-$i $i
	echo $?
done

for i in *; do
	pushd $i
	echo "Creating module.description for $i"
	modules=`find . -name "*.ko.gz"`
	echo $modules | xargs /sbin/modinfo-25 \
	| perl -lne 'print "$name\t$1" if $name && /^description:\s*(.*)/; $name = $1 if m!^filename:\s*(.*)\.k?o!; $name =~ s!.*/!!' > modules.description
	popd
done
popd

%if %build_source
# make sure we are in the directory
pushd %{target_source}
# kernel-source is shipped as an unprepared tree
%smake -s mrproper
# back to previous directory
popd
%endif # build_source


###
### scripts
###

### kernel
%preun -n %{kname}
/sbin/installkernel -R %{buildrel}
if [ -L /lib/modules/%{buildrel}/build ]; then
    rm -f /lib/modules/%{buildrel}/build
fi
if [ -L /lib/modules/%{buildrel}/source ]; then
    rm -f /lib/modules/%{buildrel}/source
fi
exit 0

%post -n %{kname}
/sbin/installkernel -L %{buildrel}
if [ -d /usr/src/%{kname}-devel-%{buildrel} ]; then
    ln -sf /usr/src/%{kname}-devel-%{buildrel} /lib/modules/%{buildrel}/build
    ln -sf /usr/src/%{kname}-devel-%{buildrel} /lib/modules/%{buildrel}/source
fi

%postun -n %{kname}
/sbin/kernel_remove_initrd %{buildrel}


### kernel-devel
%post -n %{kname}-devel
# place /build and /source symlinks in place.
if [ -d /lib/modules/%{buildrel} ]; then
    ln -sf /usr/src/%{kname}-devel-%{buildrel} /lib/modules/%{buildrel}/build
    ln -sf /usr/src/%{kname}-devel-%{buildrel} /lib/modules/%{buildrel}/source
fi

%preun -n %{kname}-devel
# we need to delete <modules>/{build,source} at uninstall
if [ -L /lib/modules/%{buildrel}/build ]; then
    rm -f /lib/modules/%{buildrel}/build
fi
if [ -L /lib/modules/%{buildrel}/source ]; then
    rm -f /lib/modules/%{buildrel}/source
fi
exit 0


### kernel-source
%post -n %{kname}-source
for i in /lib/modules/%{buildrel}*; do
	if [ -d $i ]; then
	        rm -f $i/{build,source}
	        ln -sf /usr/src/%{kname}-%{buildrel} $i/build
	        ln -sf /usr/src/%{kname}-%{buildrel} $i/source
	fi
done
								
%preun -n %{kname}-source
for i in /lib/modules/%{buildrel}/{build,source}; do
	if [ -L $i ]; then
		rm -f $i
	fi
done
exit 0
												

###
### file lists
###

#
# kernel
#
%if %build_kernel
%files -n %{kname} -f kernel_files.%{buildrel}
%endif # build_kernel

#
# kernel-source
#
%if %build_source
%files -n %{kname}-source
%defattr(-,root,root)
%dir %{_kerneldir}
%dir %{_kerneldir}/arch
%dir %{_kerneldir}/include
# this file is removed by make mrproper
#{_kerneldir}/.config
%{_kerneldir}/.gitignore
%{_kerneldir}/COPYING
%{_kerneldir}/CREDITS
%{_kerneldir}/Documentation
%{_kerneldir}/Kbuild
%{_kerneldir}/MAINTAINERS
%{_kerneldir}/Makefile
%{_kerneldir}/README
%{_kerneldir}/REPORTING-BUGS
#{_kerneldir}/Module.markers
%{_kerneldir}/arch/Kconfig
%ifarch %{ix86} x86_64
%{_kerneldir}/arch/x86
%endif
%{_kerneldir}/arch/um
%{_kerneldir}/block
%{_kerneldir}/crypto
%{_kerneldir}/drivers
%{_kerneldir}/fs
%{_kerneldir}/firmware
%{_kerneldir}/include/Kbuild
%{_kerneldir}/include/acpi
%{_kerneldir}/include/asm-generic
# this directory is not need in source rpm
#{_kerneldir}/include/config
%{_kerneldir}/include/crypto
%{_kerneldir}/include/drm
# this directory is not need in source rpm
#{_kerneldir}/include/generated
%{_kerneldir}/include/keys
%{_kerneldir}/include/linux
%{_kerneldir}/include/math-emu
%{_kerneldir}/include/media
%{_kerneldir}/include/misc
%{_kerneldir}/include/mtd
%{_kerneldir}/include/net
%{_kerneldir}/include/pcmcia
%{_kerneldir}/include/rdma
%{_kerneldir}/include/rxrpc
%{_kerneldir}/include/scsi
%{_kerneldir}/include/sound
%{_kerneldir}/include/target
%{_kerneldir}/include/trace
%{_kerneldir}/include/video
%{_kerneldir}/include/xen
%{_kerneldir}/init
%{_kerneldir}/ipc
%{_kerneldir}/Kconfig
%{_kerneldir}/kernel
%{_kerneldir}/lib
%{_kerneldir}/mm
%{_kerneldir}/net
%{_kerneldir}/samples
%{_kerneldir}/security
%{_kerneldir}/scripts
%{_kerneldir}/sound
%{_kerneldir}/tools
%{_kerneldir}/usr
%{_kerneldir}/virt
%doc README.kernel-sources
%doc README.MandrivaLinux
%endif

#
# kernel-devel
#
%if %build_devel
%files -n %{kname}-devel
%defattr(-,root,root)
%doc README.kernel-sources
%doc README.MandrivaLinux
%dir %{_develdir}
%dir %{_develdir}/arch
%dir %{_develdir}/include
%{_develdir}/.config
%{_develdir}/Documentation
%{_develdir}/Kbuild
%{_develdir}/Makefile
%{_develdir}/Module.symvers
%{_develdir}/arch/Kconfig
%ifarch %{ix86} x86_64
%{_develdir}/arch/x86
%endif
%{_develdir}/arch/um
%{_develdir}/block
%{_develdir}/crypto
%{_develdir}/drivers
%{_develdir}/firmware
%{_develdir}/fs
%{_develdir}/include/Kbuild
%{_develdir}/include/acpi
%{_develdir}/include/asm-generic
%{_develdir}/include/config
%{_develdir}/include/crypto
%{_develdir}/include/drm
%{_develdir}/include/generated
%{_develdir}/include/keys
%{_develdir}/include/linux
%{_develdir}/include/math-emu
%{_develdir}/include/media
%{_develdir}/include/misc
%{_develdir}/include/mtd
%{_develdir}/include/net
%{_develdir}/include/pcmcia
%{_develdir}/include/rdma
%{_develdir}/include/rxrpc
%{_develdir}/include/scsi
%{_develdir}/include/sound
%{_develdir}/include/target
%{_develdir}/include/trace
%{_develdir}/include/video
%{_develdir}/include/xen
%{_develdir}/init
%{_develdir}/ipc
%{_develdir}/Kconfig
%{_develdir}/kernel
%{_develdir}/lib
%{_develdir}/mm
%{_develdir}/net
%{_develdir}/samples
%{_develdir}/scripts
%{_develdir}/security
%{_develdir}/sound
%{_develdir}/tools
%{_develdir}/usr
%{_develdir}/virt
%endif # kernel_devel

#
# kernel-debug
#
%if %build_debug
%files -n %{kname}-debuginfo -f kernel_debug_files.up
%endif # build_debug


#
# kernel-doc
#
%if %build_doc
%files -n %{kname}-doc
%defattr(-,root,root)
%doc linux-%{tar_ver}/Documentation/*
%endif # kernel_doc
