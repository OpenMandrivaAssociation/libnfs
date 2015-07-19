%define	major	8
%define	libname	%mklibname nfs %{major}
%define	devname	%mklibname nfs -d

Summary:	Client library for accessing NFS shares over a network
Name:		libnfs
Version:	1.9.7
Release:	2
# examples are GPL but are not packaged
License:	LGPLv2+
Group:		System/Libraries
Url:		https://github.com/sahlberg/libnfs
Source0:	https://github.com/downloads/sahlberg/libnfs/%{name}-%{version}.tar.gz
BuildRequires:	python
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(fuse)

%description
LIBNFS is a client library for accessing NFS shares over a network.

%package -n %{libname}
Summary:	Shared library of libnfs
Group:		System/Libraries
Provides:	%{name} = %{EVRD}

%description -n %{libname}
LIBNFS is a client library for accessing NFS shares over a network.

This package contains the library needed to run programs dynamically
linked with libnfs.

%package -n %{devname}
Summary:	Headers for libnfs development
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	nfs-devel = %{EVRD}

%description -n %{devname}
This package contains the headers that are needed to develop
applications that use libnfs.

%package fuse
Summary:	An NFS implementation based on libnfs and FUSE
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}
License:	GPLv3

%description fuse
An NFS implementation based on libnfs and FUSE

%package preload
Summary:	LD_PRELOADable library for making NFS available
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}
License:	GPLv3

%description preload
A LD_PRELOADable module that can be used to make
several standard utilities nfs aware.
It is still very incomplete but can be used for basic things
such as cat and cp.
Patches to add more coverage is welcome.

You can try things like
LD_NFS_DEBUG=9 \
LD_PRELOAD=./ld_nfs.so \
cat nfs://your.server/data/tmp/foo123

LD_NFS_DEBUG=9 \
LD_PRELOAD=./ld_nfs.so \
cp nfs://your.server/data/tmp/foo123 \
   nfs://your.server/data/tmp/foo123.copy


%prep
%setup -q -n %{name}-%{name}-%{version}

%build
./bootstrap
%configure2_5x --disable-static
%make
%__cc %{optflags} -o fuse_nfs examples/fuse_nfs.c -Iinclude -Llib/.libs -lfuse -lnfs
%__cc %{optflags} -fPIC -shared -o ld_nfs.so examples/ld_nfs.c -Iinclude -Llib/.libs -ldl -lnfs

%install
%makeinstall_std
mkdir -p %{buildroot}%{_sbindir}
install -m 755 fuse_nfs %{buildroot}%{_sbindir}
install -m 755 ld_nfs.so %{buildroot}%{_libdir}

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%doc README
%{_libdir}/lib*.so
%{_includedir}/nfsc
%{_libdir}/pkgconfig/%{name}.pc

%files fuse
%{_sbindir}/fuse_nfs
%{_bindir}/nfs-ls
%{_mandir}/man1/nfs-ls.1*

%files preload
%{_libdir}/ld_nfs.so
