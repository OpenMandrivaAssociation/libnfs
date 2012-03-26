%define	major	1
%define	libname	%mklibname nfs %{major}
%define	devname	%mklibname nfs -d

Name:		libnfs
Version:	1.3.0
Release:	%mkrel 1
Summary:	Client library for accessing NFS shares over a network
# examples are GPL but are not packaged
License:	LGPLv2+
Group:		System/Libraries
URL:		https://github.com/sahlberg/libnfs
# git archive --prefix libnfs-1.3.0/ libnfs-1.3.0 | xz > libnfs-1.3.0.tar.xz
Source:		%{name}-%{version}.tar.xz
BuildRequires:	python

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
LIBNFS is a client library for accessing NFS shares over a network.

This package contains the headers that are needed to develop
applications that use libnfs.

%prep
%setup -q

%build
./bootstrap
%configure2_5x --disable-static
%make

%install
%__rm -rf %{buildroot}
%makeinstall_std

%clean
%__rm -rf %{buildroot}

%files -n %{libname}
%doc README
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%doc README
%{_libdir}/*.so
%{_includedir}/nfsc
%{_libdir}/pkgconfig/%{name}.pc
%if %{mdvver} < 201200
%{_libdir}/*.la
%endif

