#
# Note: This is not noarch, as it has %{_libdir} etc. hardcoded in *.py files
#
%define	changeset_id b6bb311c7bd3
#
Summary:	Pacemaker command line interface for management and configuration
Name:		crmsh
Version:	1.2.1
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://hg.savannah.gnu.org/hgweb/crmsh/archive/%{changeset_id}.tar.bz2
# Source0-md5:	f4d0a4d30498c3b5ee73ff8b70eb3005
Patch0:		%{name}-awk.patch
URL:		https://savannah.nongnu.org/projects/crmsh/
BuildRequires:	asciidoc
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	docbook-dtd45-xml
BuildRequires:	pacemaker-devel >= 1.1.8
BuildRequires:	python
BuildRequires:	python-modules
Requires:	pacemaker >= 1.1.8
Provides:	pacemaker-shell
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pacemaker command line interface for management and configuration.

Contains the 'crm' utility which was part of Pacemaker < 1.1.8

%prep
%setup -qn %{name}-%{changeset_id}
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
%attr(755,root,root) %{_sbindir}/crm
%{py_sitedir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man8/crm.8*
