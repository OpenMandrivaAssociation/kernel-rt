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
%define kstable		34

%define ktag		rt

# AKPM's release
%define rt_rel		51

# this is the releaseversion
%define mdvrelease 	1

# This is only to make life easier for people that creates derivated kernels
# a.k.a name it kernel-tmb :)
%define kname 		kernel-%{ktag}

%define rpmtag		%distsuffix
%if %kpatch
%define rpmrel		0.%{kpatch}.%{ktag}%{rt_rel}.%{mdvrelease}
%else
%define rpmrel		1.%{ktag}%{rt_rel}.%{mdvrelease}
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
%define requires1 module-init-tools >= 3.0-7
%define requires2 mkinitrd >= 3.4.43-10
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
URL: 		https://www.kernel.org/
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
Source0:        ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.x/linux-%{tar_ver}.tar.xz
Source1:        ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.x/linux-%{tar_ver}.tar.sign
# This is for disabling mrproper on -devel rpms
Source2:	disable-mrproper-in-devel-rpms.patch
# This disables removal of bounds.h and asm-offsets.h in -devel rpms (from kernel-linus)
#SOURCE3:	kbuild-really-dont-remove-bounds-asm-offsets-headers.patch

Source4:  README.kernel-sources
Source5:  README.MandrivaLinux

Source6:  %{name}.rpmlintrc

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
Patch1:         ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.x/testing/patch-%{kernelversion}.%{patchlevel}-%{kpatch}.xz
Source10:       ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.x/testing/patch-%{kernelversion}.%{patchlevel}-%{kpatch}.sign
%endif
%if %kstable
Patch1:         ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.x/patch-%{kversion}.xz
Source10:       ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.x/patch-%{kversion}.sign
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
Obsoletes: %{kname}-latest < %{EVRD}

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
Obsoletes: %{kname}-source-latest < %{EVRD}

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
Obsoletes: %{kname}-devel-latest < %{EVRD}

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

sed -i '/^LD/s/ld$/ld.bfd/' %{build_dir}/linux-%{tar_ver}/Makefile

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
# Needed for truecrypt build (Danny)
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


%changelog
* Wed Sep 05 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.28-1.rt42.1
+ Revision: 816391
- update to 3.2.28-rt42

* Tue Aug 07 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.26-1.rt39.1
+ Revision: 811939
- 3.2.26-rt39 release
- use ld.bfd for linking because ld.gold fails on i386
- add rpmlintrc
- update to 3.2.23-rt37
- obsolete kernel-rt*-latest packages

* Wed Jul 11 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.22-1.rt34.1
+ Revision: 808874
- update to 3.2.22-rt34

* Wed Jun 27 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.21-1.rt33.1
+ Revision: 807190
- update to 3.2.21-rt33

* Wed May 30 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.18-1.rt29.1
+ Revision: 801227
- update to 3.2.18-rt29

* Mon May 21 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.17-1.rt28.1
+ Revision: 799758
- update to 3.2.17-rt28

* Tue Apr 24 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.16-1.rt27.1
+ Revision: 793113
- update to 3.2.16-rt27

* Fri Apr 20 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.15-1.rt26.1
+ Revision: 792452
- update to 3.2.15-rt26

* Tue Apr 10 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.14-1.rt24.1
+ Revision: 790245
- update to 3.2.14-rt24

* Wed Apr 04 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.13-1.rt23.1
+ Revision: 789115
- update to 3.2.13-rt23
- remove %%mkrel macro

* Thu Mar 29 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.12-1.rt22.1
+ Revision: 788128
- update to 3.2.12-rt22

* Wed Mar 14 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.11-1.rt20.1
+ Revision: 784933
- update to 3.2.11-rt20

* Tue Mar 13 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.10-1.rt18.1
+ Revision: 784690
- update to 3.2.10-rt18

* Mon Mar 05 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.9-1.rt15.1
+ Revision: 782141
- new version 3.2.9-rt15

* Fri Mar 02 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.9-1.rt14.1
+ Revision: 781790
- new version 3.2.9-rt14

* Fri Feb 17 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.6-1.rt13.1
+ Revision: 776098
- new version 3.2.6-rt13

* Fri Feb 10 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.5-1.rt12.1
+ Revision: 772417
- update to 3.2.5-rt12

* Mon Jan 23 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.0-1.rt10.1
+ Revision: 766790
- specfile cleanup
- re-enable modules gzipping
- add new tarballs
- fix errors related to depmod
- new version 3.2-rt10
- various fixes in spec file
- update source files
- New version 3.2-rc6-rt9
  *-latest packages dropped
  fake version and release numbers removed

  + trem <trem@mandriva.org>
    - update to 2.6.33.7-rt29

* Wed Jul 14 2010 trem <trem@mandriva.org> 2.6.33.6-1.rt26.1mdv2011.0
+ Revision: 553407
- update to 2.6.33.6-rt26

* Wed Jun 09 2010 trem <trem@mandriva.org> 2.6.33.5-1.rt23.1mdv2010.1
+ Revision: 547802
- update to 2.6.33.5-rt23
- add patch video-fb-fix-unregister_framebuffer-fb_destroy.patch from "officiel" kernel
- disable CONFIG_CC_OPTIMIZE_FOR_SIZE and CONFIG_VGACON_SOFT_SCROLLBACK
- update to 2.6.33.5-rt22

* Wed May 19 2010 trem <trem@mandriva.org> 2.6.33.4-1.rt20.1mdv2010.1
+ Revision: 545454
- update to 2.6.33.4-rt20

* Sun May 02 2010 trem <trem@mandriva.org> 2.6.33.3-1.rt19.1mdv2010.1
+ Revision: 541693
- update to 2.6.33.3-rt19

* Sat May 01 2010 trem <trem@mandriva.org> 2.6.33.3-1.rt17.2mdv2010.1
+ Revision: 541394
- include agp in the kernel (it avoid dependancy problem when building the initrd)

* Fri Apr 30 2010 trem <trem@mandriva.org> 2.6.33.3-1.rt17.1mdv2010.1
+ Revision: 541376
- update to 2.6.33.3-rt17
- remove fix_namei.patch and fix_fs_ecryptfs_inode_c.patch (added upstream)

* Thu Apr 29 2010 trem <trem@mandriva.org> 2.6.33.3-1.rt16.2mdv2010.1
+ Revision: 541046
- add 2 patches for the nouveau driver (thanks tmb for the information)

* Thu Apr 29 2010 trem <trem@mandriva.org> 2.6.33.3-1.rt16.1mdv2010.1
+ Revision: 540680
- add 2 simple patch to fix the compilation
- enable nouveau
- update to 2.6.33.3-rt16

* Sat Apr 10 2010 trem <trem@mandriva.org> 2.6.33.2-1.rt13.1mdv2010.1
+ Revision: 533547
- update to 2.6.33.2-rt13

* Wed Mar 24 2010 trem <trem@mandriva.org> 2.6.33.1-1.rt11.1mdv2010.1
+ Revision: 526983
- update to 2.6.33.1-rt11

* Thu Mar 18 2010 trem <trem@mandriva.org> 2.6.33.1-1.rt10.1mdv2010.1
+ Revision: 524745
- update to 2.6.33.1-rt10
- remove patch wtf.diff (added upstream)
- update to 2.6.33.1-rt9
- add patch wtf.diff that fix compilation for i915

* Fri Mar 12 2010 trem <trem@mandriva.org> 2.6.33-1.rt7.1mdv2010.1
+ Revision: 518569
- update to 2.6.33-rt7

* Mon Mar 01 2010 trem <trem@mandriva.org> 2.6.33-1.rt4.1mdv2010.1
+ Revision: 513032
- update to 2.6.33-rt4

* Sun Feb 28 2010 trem <trem@mandriva.org> 2.6.33-1.rt3.1mdv2010.1
+ Revision: 512807
- update to 2.6.33-rt3

* Thu Feb 18 2010 trem <trem@mandriva.org> 2.6.31.12-1.rt21.1mdv2010.1
+ Revision: 507925
- update to 2.6.31.12-rt21

* Thu Feb 11 2010 trem <trem@mandriva.org> 2.6.31.12-1.rt20.2mdv2010.1
+ Revision: 504344
- set RTC_HCTOSYS

* Sat Jan 23 2010 trem <trem@mandriva.org> 2.6.31.12-1.rt20.1mdv2010.1
+ Revision: 495303
- update to 2.6.31.12-rt20

* Wed Nov 11 2009 trem <trem@mandriva.org> 2.6.31.6-1.rt19.1mdv2010.1
+ Revision: 464395
- update to 2.6.31.6-rt19

* Sat Nov 07 2009 trem <trem@mandriva.org> 2.6.31.5-1.rt18.1mdv2010.1
+ Revision: 462396
- update to 2.6.31.5-rt18

* Wed Oct 14 2009 trem <trem@mandriva.org> 2.6.31.4-1.rt14.1mdv2010.0
+ Revision: 457307
- update to 2.6.31.4-rt14

* Tue Oct 06 2009 trem <trem@mandriva.org> 2.6.31.2-1.rt13.1mdv2010.0
+ Revision: 454703
- update to 2.6.31.2-rt13

* Sun Sep 20 2009 trem <trem@mandriva.org> 2.6.31-1.rt11.1mdv2010.0
+ Revision: 444794
- update to 2.6.31-rt11

* Tue Sep 15 2009 trem <trem@mandriva.org> 2.6.31-1.rt10.1mdv2010.0
+ Revision: 443297
- update to 2.6.31-rt10

* Fri Sep 11 2009 trem <trem@mandriva.org> 2.6.31-0.rc9.rt9.1.1mdv2010.0
+ Revision: 438525
- update to 2.6.31-rc9-rt9.1

* Mon Aug 31 2009 trem <trem@mandriva.org> 2.6.31-0.rc8.rt9.2mdv2010.0
+ Revision: 423112
- remove CONFIG_SYSFS?\195?\168DEPRECATED

* Sat Aug 29 2009 trem <trem@mandriva.org> 2.6.31-0.rc8.rt9.1mdv2010.0
+ Revision: 422067
- update to 2.6.31-rc8-rt9

* Wed Aug 26 2009 trem <trem@mandriva.org> 2.6.31-0.rc7.rt8.1mdv2010.0
+ Revision: 421579
- update to 2.6.31-rc7-rt8

* Tue Aug 25 2009 trem <trem@mandriva.org> 2.6.31-0.rc7.rt7.1mdv2010.0
+ Revision: 421291
- update to 2.6.31-rc7-rt7

* Sun Aug 23 2009 trem <trem@mandriva.org> 2.6.31-0.rc6.rt6.1mdv2010.0
+ Revision: 419740
- update to 2.6.31-rc6-rt6

* Thu Aug 20 2009 trem <trem@mandriva.org> 2.6.31-0.rc6.rt5.2mdv2010.0
+ Revision: 418595
- update disable-mrproper-in-devel-rpms.patch
- add kbuild-really-dont-remove-bounds-asm-offsets-headers.patch (from kernel-linus)
- update to 2.6.31-rc6-rt5

* Wed Aug 19 2009 trem <trem@mandriva.org> 2.6.31-0.rc6.rt4.1mdv2010.0
+ Revision: 417893
- update to 2.6.31-rc6-rt4

* Mon Aug 17 2009 trem <trem@mandriva.org> 2.6.31-0.rc6.rt2.1mdv2010.0
+ Revision: 417177
- update to 2.6.31-rc6-rt2

* Thu Aug 13 2009 trem <trem@mandriva.org> 2.6.31-0.rc5.rt1.2.1mdv2010.0
+ Revision: 415793
- update to unofficial 2.6.31.rc5-rt1.2

* Thu Aug 06 2009 trem <trem@mandriva.org> 2.6.31-0.rc5.rt1.1.2mdv2010.0
+ Revision: 410986
- update to non-official 2.6.31-rc5-rt1.1

* Thu Aug 06 2009 trem <trem@mandriva.org> 2.6.31-0.rc4.rt1.2mdv2010.0
+ Revision: 410410
- add "arch/x86/include" in -devel

* Tue Aug 04 2009 trem <trem@mandriva.org> 2.6.31-0.rc4.rt1.1mdv2010.0
+ Revision: 408626
- update to 2.6.31-rc4-rt1

* Fri Jul 10 2009 trem <trem@mandriva.org> 2.6.29.6-1.rt23.1mdv2010.0
+ Revision: 394212
- update to 2.6.29.6-rt23

* Tue Jun 23 2009 trem <trem@mandriva.org> 2.6.29.5-1.rt22.1mdv2010.0
+ Revision: 388723
- update to 2.6.29.5-rt22

* Wed Jun 17 2009 trem <trem@mandriva.org> 2.6.29.5-1.rt21.1mdv2010.0
+ Revision: 386757
- update to 2.6.29.5-rt21

* Mon Jun 15 2009 trem <trem@mandriva.org> 2.6.29.4-1.rt19.1mdv2010.0
+ Revision: 386169
- update to 2.6.29.4-rt19
- remove patch smi-detector.patch (added upstream)

* Thu Jun 04 2009 trem <trem@mandriva.org> 2.6.29.4-1.rt16.2mdv2010.0
+ Revision: 382892
- add smi detector patch

* Mon May 25 2009 trem <trem@mandriva.org> 2.6.29.4-1.rt16.1mdv2010.0
+ Revision: 379659
- update to 2.6.29.4-rt16
- update to 2.6.29.4-rt15

* Tue May 19 2009 trem <trem@mandriva.org> 2.6.29.3-1.rt14.1mdv2010.0
+ Revision: 377788
- update to 2.6.29.3-rt14

* Fri May 15 2009 trem <trem@mandriva.org> 2.6.29.3-1.rt13.2mdv2010.0
+ Revision: 376281
- set HZ to 1000 (instead of 250)

* Wed May 13 2009 trem <trem@mandriva.org> 2.6.29.3-1.rt13.1mdv2010.0
+ Revision: 375585
- update to 2.6.29.3-rt13

* Sun May 03 2009 trem <trem@mandriva.org> 2.6.29.2-1.rt11.1mdv2010.0
+ Revision: 370818
- update to 2.6.29.2-rt11

* Wed Apr 29 2009 trem <trem@mandriva.org> 2.6.29.2-1.rt10.1mdv2010.0
+ Revision: 369146
- update to 2.6.29.2-rt10
- update to 2.6.29.1-rt9
- fix Group :
 Development/Debug for debug and debug-latest
 Books/Computer books for doc and doc-latest
 Development/Kernel for all others

* Sat Apr 18 2009 trem <trem@mandriva.org> 2.6.29.1-1.rt8.1mdv2009.1
+ Revision: 367982
- update to 2.6.29.1-rt8

* Fri Apr 03 2009 trem <trem@mandriva.org> 2.6.29.1-1.rt4.1mdv2009.1
+ Revision: 363889
- update to 2.6.29.1-rt4
- update to 2.6.29-rt3

* Sun Mar 29 2009 trem <trem@mandriva.org> 2.6.29-1.rt1.1mdv2009.1
+ Revision: 362119
- update to 2.6.29-rt1
- update to 2.6.29-rc7-rt1

* Wed Feb 25 2009 trem <trem@mandriva.org> 2.6.29-0.rc6.rt3.1mdv2009.1
+ Revision: 344617
- update to 2.6.29-rc6-rt3

* Sun Feb 15 2009 trem <trem@mandriva.org> 2.6.26.8-1.rt16.1mdv2009.1
+ Revision: 340495
- update to 2.6.26.8-rt16

* Sat Jan 31 2009 trem <trem@mandriva.org> 2.6.26.8-1.rt15.1mdv2009.1
+ Revision: 335803
- update to 2.6.26.8-rt15

* Wed Jan 14 2009 trem <trem@mandriva.org> 2.6.26.8-1.rt13.2mdv2009.1
+ Revision: 329618
- use smp config (and not up config)
- remove smp kernel, only use one kernel-rt for both up and smp

* Sat Jan 10 2009 trem <trem@mandriva.org> 2.6.26.8-1.rt13.1mdv2009.1
+ Revision: 327991
- update 2.6.26.8-rt13

* Mon Dec 22 2008 trem <trem@mandriva.org> 2.6.26.8-1.rt12.1mdv2009.1
+ Revision: 317715
- update to 2.6.26.8-rt12

* Sun Nov 02 2008 trem <trem@mandriva.org> 2.6.26.6-1.rt11.2mdv2009.1
+ Revision: 299193
- add debug info on module (same way as the mdv kernel)

* Tue Oct 14 2008 trem <trem@mandriva.org> 2.6.26.6-1.rt11.1mdv2009.1
+ Revision: 293770
- update to 2.6.26.6-rt11
- update to 2.6.26.6-rt10

* Thu Sep 11 2008 trem <trem@mandriva.org> 2.6.26.5-1.rt9.1mdv2009.0
+ Revision: 283938
- update to 2.6.26.5-rt9

* Wed Sep 10 2008 trem <trem@mandriva.org> 2.6.26.5-1.rt8.1mdv2009.0
+ Revision: 283604
- update to 2.6.26.5-rt8

* Mon Sep 08 2008 trem <trem@mandriva.org> 2.6.26.3-1.rt7.3mdv2009.0
+ Revision: 282794
- add kernel-firmware as require for kernel-rt-smp too

* Mon Sep 08 2008 trem <trem@mandriva.org> 2.6.26.3-1.rt7.2mdv2009.0
+ Revision: 282756
- add kernel-firmware as requires

* Sat Sep 06 2008 trem <trem@mandriva.org> 2.6.26.3-1.rt7.1mdv2009.0
+ Revision: 281843
- update to 2.6.26.3-rt7
- update to 2.6.26.3-rt6

* Thu Sep 04 2008 trem <trem@mandriva.org> 2.6.26.3-1.rt5.1mdv2009.0
+ Revision: 280813
- update to 2.6.26.3-rt5
- add include/trace/sched.h to source and devel
- update to 2.6.26.3-rt4

* Sat Aug 23 2008 trem <trem@mandriva.org> 2.6.26.3-1.rt3.1mdv2009.0
+ Revision: 275315
- remove Module.markers from source rpm
- update to 2.6.26.3-rt3
- remove patch fix_infiniband.patch and fix_isp1760.patch

* Sat Aug 16 2008 trem <trem@mandriva.org> 2.6.26-1.rt1.1mdv2009.0
+ Revision: 272608
- fix patch disable-mrproper-in-devel-rpms.patch
- remove sigframe_32.h from devel (this file no more exist)
- add patch fix_infiniband.patch and fix_isp1760.patch
- update to 2.6.26-rt1

* Tue Jun 24 2008 trem <trem@mandriva.org> 2.6.25.8-1.rt7.1mdv2009.0
+ Revision: 228750
- update to 2.6.25.8-rt7

* Sun Jun 08 2008 trem <trem@mandriva.org> 2.6.25.4-1.rt6.1mdv2009.0
+ Revision: 216836
- update to 2.6.25.4-rt3
- disable CONFIG_RT_GROUP_SCHED (break the compilation)

* Tue May 20 2008 trem <trem@mandriva.org> 2.6.25.4-1.rt3.1mdv2009.0
+ Revision: 209549
- update to 2.6.25.4-rt3

* Sun May 18 2008 trem <trem@mandriva.org> 2.6.25.4-1.rt1.1mdv2009.0
+ Revision: 208737
- remove arch/i386 from kernel source
- update to 2.6.25.4-rt1

* Sat May 17 2008 trem <trem@mandriva.org> 2.6.24.7-1.rt6.1mdv2009.0
+ Revision: 208442
- update to 2.6.24.7-rt6

  + Thomas Backlund <tmb@mandriva.org>
    - update to 2.6.24.4-rt4
    - fix license

* Thu Feb 28 2008 trem <trem@mandriva.org> 2.6.24.3-1.rt3.2mdv2008.1
+ Revision: 175958
- update to 2.6.24.3-rt3

* Fri Feb 22 2008 trem <trem@mandriva.org> 2.6.24.2-1.rt2.2mdv2008.1
+ Revision: 174020
- update to 2.6.24.2-rt2

* Thu Jan 31 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24-1.rt1.2mdv2008.1
+ Revision: 160945
- add kernel-sysctl_check-remove-s390-include.patch (#37388)

* Sat Jan 26 2008 trem <trem@mandriva.org> 2.6.24-1.rt1.1mdv2008.1
+ Revision: 158285
- update to 2.6.24-rt1

* Thu Jan 17 2008 trem <trem@mandriva.org> 2.6.24-0.rc8.rt1.1mdv2008.1
+ Revision: 154478
- update to 2.6.24-rc8-rt1

* Sun Jan 13 2008 trem <trem@mandriva.org> 2.6.24-0.rc7.rt1.1mdv2008.1
+ Revision: 151054
- add patch to fix quicklist.h
- update to 2.6.24-rc7-rt1

* Wed Jan 02 2008 trem <trem@mandriva.org> 2.6.24-0.rc5.rt1.2mdv2008.1
+ Revision: 140734
- add -debug package with vmlinux file (used by oprofile, systemtap, ...)

  + Thomas Backlund <tmb@mandriva.org>
    - update source2 to apply cleanly
    - fix kernelupdate symlink

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Dec 15 2007 trem <trem@mandriva.org> 2.6.24-0.rc5.rt1.1mdv2008.1
+ Revision: 120292
- fix compilation on i586
- update to 2.6.24-rc5-rt1

  + Thomas Backlund <tmb@mandriva.org>
    - call installkernel with -L to avoid changing main kernel
      default symlinks

* Mon Nov 19 2007 trem <trem@mandriva.org> 2.6.24-0.rc2.rt1.3mdv2008.1
+ Revision: 110554
- disable mrproper target on -devel rpms to stop 3rdparty installers
  from wiping out needed files and thereby breaking builds
  (based on an initial patch by Danny used in kernel-multimedia series)
- fix build of kernel source

* Mon Nov 19 2007 Thierry Vignaud <tv@mandriva.org> 2.6.24-0.rc2.rt1.2mdv2008.1
+ Revision: 110403
- fix build

  + trem <trem@mandriva.org>
    - fix compilation on i586 (user %%{_arch} instead of %%{targer_cpu})
    - update to 2.6.24-rc2-rt1
    - add two patches to fix compilation (ioat_dma.c and kvm_main.c)

* Thu Nov 08 2007 trem <trem@mandriva.org> 2.6.23.1-1.rt11.1mdv2008.1
+ Revision: 106843
- update to 2.6.23.1-rt11

* Mon Oct 29 2007 trem <trem@mandriva.org> 2.6.23.1-1.rt5.1mdv2008.1
+ Revision: 103630
- update to 2.6.23.1-rt5

* Sun Oct 28 2007 trem <trem@mandriva.org> 2.6.23.1-1.rt4.1mdv2008.1
+ Revision: 102811
- update to 2.6.23.1-rt4

* Thu Oct 25 2007 trem <trem@mandriva.org> 2.6.23-1.rt3.1mdv2008.1
+ Revision: 102207
- update to 2.6.23-rt3

* Wed Oct 24 2007 trem <trem@mandriva.org> 2.6.23-1.rt2.1mdv2008.1
+ Revision: 101903
- update to 2.6.23-rt2

* Wed Oct 17 2007 trem <trem@mandriva.org> 2.6.23-1.rt1.1mdv2008.1
+ Revision: 99735
- now, we use 1. for stable release (we continue to use 0. for unstable release)
- update to 2.6.23-rt1

* Tue Oct 09 2007 trem <trem@mandriva.org> 2.6.23-0.rc9.rt2.2mdv2008.1
+ Revision: 96319
- update to 2.6.23-rc9-rt2

* Thu Sep 27 2007 trem <trem@mandriva.org> 2.6.23-0.rc8.rt1.2mdv2008.0
+ Revision: 93206
- update to 2.6.23-rc8-rt1

* Thu Sep 06 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23-0.rc4.rt1.2mdv2008.0
+ Revision: 81324
- rebuild as the old one got lost in the BS

* Sun Sep 02 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23-0.rc4.rt1.1mdv2008.0
+ Revision: 77737
- update to kernel.org 2.6.23-rc4
- update to 2.6.23-rc4-rt1
- fix #29744, #29074 in a cleaner way by disabling the sourcing of
  arch/s390/crypto/Kconfig
- fix patch urls to match the new project repo at kernel.org
- drop patches 3, 4
- update defconfigs

* Fri Aug 10 2007 trem <trem@mandriva.org> 2.6.23-0.rc2.rt2.1mdv2008.0
+ Revision: 61661
- update to 2.6.23-rc2-rt2

* Tue Aug 07 2007 trem <trem@mandriva.org> 2.6.22.1-rt9.2mdv2008.0
+ Revision: 59994
- new mdv packaging (2mdv)
- disable CONFIG_DEBUG_LOCK_ALLOC and CONFIG_PROVE_LOCKING in i386-smp.config (was forgotten)

* Sat Jul 28 2007 trem <trem@mandriva.org> 2.6.22.1-rt9.1mdv2008.0
+ Revision: 56455
- update to release 2.6.22.1-rt9
- disable : CONFIG_CPU_IDLE, CONFIG_DEBUG_LOCK_ALLOC, CONFIG_PROVE_LOCKING
- update to 2.6.22.1-rt6

* Sun Jul 15 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22.1-rt3.2mdv2008.0
+ Revision: 52298
- disable LOCKDEP and DEBUG_SLAB as they are bad for latencies and runtime overhead
- fix build when building only up or smp

* Sat Jul 14 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22.1-rt3.1mdv2008.0
+ Revision: 52083
- use defconfigs from kernel-linus-2.6.22.1, and adapt them for
  realtime build
- dont build -doc rpms
- Introduce Ingo Molnars kernel-rt (realtime) series
- Created package structure for kernel-rt.

