%define major 5
%define libname %mklibname nfc %{major}
%define devname %mklibname -d nfc

Name:		libnfc
Version:	1.8.0
Release:	2
Summary:	NFC SDK and Programmers API

Group:		System/Libraries
License:	LGPLv3+
URL:		http://www.libnfc.org/
Source0:	https://github.com/nfc-tools/libnfc/archive/%{name}-%{version}.tar.gz

BuildRequires:	pkgconfig(libpcsclite)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	cmake
Requires(post):	rpm-helper
Requires(postun): rpm-helper

%description
libnfc is the first free NFC SDK and Programmers API released under the
GNU Lesser General Public License. It provides complete transparency and
royalty-free use for everyone.

%package -n	%{libname}
Summary:	NFC SDK and Programmers API
Group:		System/Libraries

%description -n %{libname}
libnfc is the first free NFC SDK and Programmers API released under the
GNU Lesser General Public License. It provides complete transparency and
royalty-free use for everyone.

%package -n	%{devname}
Summary:	Development libraries for libnfc
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
The libnfc-devel package contains header files necessary for
developing programs using libnfc.

%package	examples
Summary:	Examples using libnfc
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}

%description	examples
The libnfc-examples package contains examples demonstrating the functionality
of libnfc.

%prep
%autosetup -n %{name}-%{name}-%{version}

%build
%cmake
%make_build

%install
%makeinstall_std -C build

# install udev rule
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d/
install -p -m 0644 contrib/udev/*-pn53x.rules %{buildroot}%{_sysconfdir}/udev/rules.d/

# fix typo in sample config file (reported upstream - issue 247)
sed -i 's/allow_intrusive_autoscan/allow_intrusive_scan/g' libnfc.conf.sample

# install sample config file
mkdir -p %{buildroot}%{_sysconfdir}/nfc/devices.d
install -p -m 0644 libnfc.conf.sample %{buildroot}%{_sysconfdir}/nfc/libnfc.conf

%files
%dir %{_sysconfdir}/nfc
%dir %{_sysconfdir}/nfc/devices.d
%config(noreplace) %{_sysconfdir}/udev/rules.d/*-pn53x.rules
%config(noreplace) %{_sysconfdir}/nfc/libnfc.conf
%doc COPYING AUTHORS ChangeLog

%files -n %{libname}
%{_libdir}/*.so.*

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/nfc/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/%{name}/*.cmake

%files examples
%{_bindir}/*
%{_mandir}/man1/*
