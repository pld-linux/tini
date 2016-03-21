#
# Conditional build:
%bcond_without	static		# don't build static version

Summary:	A tiny but valid init process for containers
Name:		tini
Version:	0.9.0
Release:	1
License:	MIT
Group:		Base
Source0:	https://github.com/krallin/tini/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	efd014cf45babe76415c4d6caee643d8
URL:		https://github.com/krallin/tini
BuildRequires:	cmake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tini is the simplest init you could think of.

All Tini does is spawn a single child (Tini is meant to be run in a
container), and wait for it to exit all the while reaping zombies and
performing signal forwarding.

%package static
Summary:	Statically linked tini
Group:		Base

%description static
Statically linked tini.

%prep
%setup -q

%build
install -d build
cd build
%cmake ..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE
%attr(755,root,root) %{_bindir}/tini

%files static
%defattr(644,root,root,755)
%doc LICENSE
%attr(755,root,root) %{_bindir}/tini-static
