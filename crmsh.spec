#
# Note: This is not noarch, as it has %{_libdir} etc. hardcoded in *.py files
#
Summary:	Pacemaker command line interface for management and configuration
Summary(pl.UTF-8):	Interfejs linii poleceń do zarządzania i konfiguracji Pacemakera
Name:		crmsh
Version:	3.0.0
Release:	1
License:	GPL v2+
Group:		Applications/System
#Source0Download: https://github.com/ClusterLabs/crmsh/releases
Source0:	https://github.com/ClusterLabs/crmsh/archive/%{version}/crmsh-%{version}.tar.gz
# Source0-md5:	ff41cc2f4abf4498ea55fe033eb854f3
Patch0:		%{name}-awk.patch
URL:		http://crmsh.github.io/
BuildRequires:	asciidoc
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	docbook-dtd45-xml
BuildRequires:	python >= 1:2.6
BuildRequires:	python-modules >= 1:2.6
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
%patch0 -p1

%{__sed} -i -e '1s,/usr/bin/env python,%{__python},' \
	utils/crm_clean.py \
	scripts/check-uptime/*.py \
	scripts/health/*.py

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
# can we py_postclean?

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}
# tests
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/tests
# reduntant
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/crmsh/install_files.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md TODO doc/*.html
%dir /etc/crm
%config(noreplace) %verify(not md5 mtime size) /etc/crm/crm.conf
%attr(755,root,root) %{_bindir}/crm
%{py_sitedir}/crmsh
%{py_sitedir}/crmsh-%{version}-py*.egg-info
%{_datadir}/%{name}
%{_mandir}/man8/crm.8*
%{_mandir}/man8/crmsh_hb_report.8*
