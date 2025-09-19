#
# Note: This is not noarch, as it has %{_libdir} etc. hardcoded in *.py files
%define		_enable_debug_packages	0
#
Summary:	Pacemaker command line interface for management and configuration
Summary(pl.UTF-8):	Interfejs linii poleceń do zarządzania i konfiguracji Pacemakera
Name:		crmsh
Version:	5.0.0
Release:	1
License:	GPL v2+
Group:		Applications/System
#Source0Download: https://github.com/ClusterLabs/crmsh/releases
Source0:	https://github.com/ClusterLabs/crmsh/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d38e3073d35d56c3aff15efa6680a7ee
Patch0:		%{name}-awk.patch
Patch1:		no-venv.patch
Patch2:		pip-install.patch
URL:		http://crmsh.github.io/
BuildRequires:	asciidoc
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	docbook-dtd45-xml
BuildRequires:	python3
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
Requires:	cluster-glue
Requires:	pacemaker >= 1.1.11
Provides:	pacemaker-shell
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pacemaker command line interface for management and configuration.

Contains the 'crm' utility which was part of Pacemaker < 1.1.8.

%description -l pl.UTF-8
Interfejs linii poleceń do zarządzania i konfiguracji Pacemakera.

Zawiera polecenie "crm", które było częścią Pacemakera < 1.1.8.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python(\s|$),#!%{__python3}\1,' -e '1s,#!\s*/usr/bin/python(\s|$),#!%{__python3}\1,' \
      utils/crm_clean.py \
      utils/crm_pkg.py \
      utils/crm_rpmcheck.py \
      scripts/check-uptime/*.py \
      scripts/health/*.py \
      bin/crm

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	PYTHON=%{__python3}
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}
# tests
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md TODO doc/*.html
%dir %{_sysconfdir}/crm
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/crm/crm.conf
%{_sysconfdir}/crm/profiles.yml
%attr(755,root,root) %{_bindir}/crm
%{py3_sitescriptdir}/crmsh
%{py3_sitescriptdir}/crmsh-%{version}.dist-info
%{_datadir}/%{name}
%{_mandir}/man8/crm.8*
%{_mandir}/man8/crmsh_crm_report.8*
%{_mandir}/man8/profiles.8*
