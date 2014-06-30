#
# Note: This is not noarch, as it has %{_libdir} etc. hardcoded in *.py files
#
Summary:	Pacemaker command line interface for management and configuration
Name:		crmsh
Version:	2.1.0
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	https://github.com/crmsh/crmsh/archive/%{version}/crmsh-%{version}.tar.gz
# Source0-md5:	2b7c39a561f59d146882f4c020fa9060
Patch0:		%{name}-awk.patch
URL:		http://crmsh.github.io/
BuildRequires:	asciidoc
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cluster-glue-libs-devel
BuildRequires:	docbook-dtd45-xml
BuildRequires:	pacemaker-devel >= 1.1.8
BuildRequires:	python
BuildRequires:	python-modules
Requires:	pacemaker >= 1.1.11
Provides:	pacemaker-shell
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pacemaker command line interface for management and configuration.

Contains the 'crm' utility which was part of Pacemaker < 1.1.8

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README doc/*.html
%dir /etc/crm
%config(noreplace) %verify(not md5 mtime size) /etc/crm/crm.conf
%attr(755,root,root) %{_sbindir}/crm
%{py_sitedir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man8/crm.8*
%{_mandir}/man8/crmsh_hb_report.8.gz
