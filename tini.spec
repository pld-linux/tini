# TODO
# - build static with musl (800kb static binary vs 19k dynamic)
#
# Conditional build:
%bcond_without	static		# don't build static version
%bcond_without	tests		# Smoke tests (actual tests need Docker to run)

Summary:	A tiny but valid init process for containers
Name:		tini
Version:	0.13.0
Release:	1
License:	MIT
Group:		Base
Source0:	https://github.com/krallin/tini/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c29541112a242c53c82bb6b1213f288f
URL:		https://github.com/krallin/tini
BuildRequires:	cmake
%{?with_static:BuildRequires:	glibc-static}
BuildRequires:	xxd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
Tini is the simplest init you could think of.

All Tini does is spawn a single child (Tini is meant to be run in a
container), and wait for it to exit all the while reaping zombies and
performing signal forwarding.

%package static
Summary:	Statically linked tini
Group:		Base

%description static
Tini is the simplest init you could think of.

All Tini does is spawn a single child (Tini is meant to be run in a
container), and wait for it to exit all the while reaping zombies and
performing signal forwarding.

This package contains statically linked tini. The dynamically linked
tini uses only libc, so using statically linked program makes only
sense if you do not use libc in your container.

%prep
%setup -q

%build
install -d build
cd build
%cmake ..
%{__make}

%if %{with tests}
# Smoke tests
for tini in ./tini %{?with_static:./tini-static}; do
	echo "Smoke test for $tini"
	$tini -h

	echo "Testing $tini with: true"
	$tini -vvv true

	echo "Testing $tini with: false"
	if $tini -vvv false; then
		exit 1
	fi

	# Test stdin / stdout are handed over to child
	echo "Testing pipe"
	echo "exit 0" | $tini -vvv sh
	if [ ! "$?" -eq "0" ]; then
		echo "Pipe test failed"
		exit 1
	fi

#	echo "Checking hardening on $tini"
#	hardening-check --nopie --nostackprotector --nobindnow $tini
done
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sbindir}
mv $RPM_BUILD_ROOT{%{_bindir}/*,%{_sbindir}}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE
%attr(755,root,root) %{_sbindir}/tini

%files static
%defattr(644,root,root,755)
%doc LICENSE
%attr(755,root,root) %{_sbindir}/tini-static
