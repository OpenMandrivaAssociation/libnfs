%define	major	8
%define	libname	%mklibname nfs %{major}
%define	devname	%mklibname nfs -d

Summary:	Client library for accessing NFS shares over a network
Name:		libnfs
Version:	4.0.0
Release:	1
# examples are GPL but are not packaged
License:	LGPLv2+
Group:		System/Libraries
Url:		https://github.com/sahlberg/libnfs
Source0:	https://github.com/sahlberg/libnfs/archive/refs/tags/%{name}-%{name}-%{version}.tar.gz
BuildRequires:	python
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(fuse)

%description
LIBNFS is a client library for accessing NFS shares over a network.

%package -n %{libname}
Summary:	Shared library of libnfs
Group:		System/Libraries
Provides:	%{name} = %{EVRD}
Obsoletes:	%{name}-preload < %{EVRD}

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

%package utils
Summary:	Utils for libnfs
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}
Conflicts:	%{name}-fuse < %{EVRD}
License:	GPLv3

%description utils
Utilities for libnfs.

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
%configure --disable-static
%make_build

%install
%make_install
mkdir -p %{buildroot}%{_sbindir}

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%doc README
%{_libdir}/lib*.so
%{_includedir}/nfsc
%{_libdir}/pkgconfig/%{name}.pc

%files utils
%{_bindir}/nfs-ls
%{_bindir}/nfs-cat
%{_bindir}/nfs-cp
%{_mandir}/man1/nfs-cat.1*
%{_mandir}/man1/nfs-cp.1*
%{_mandir}/man1/nfs-ls.1*

