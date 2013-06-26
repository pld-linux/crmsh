#
# Note: This is not noarch, as it has %{_libdir} etc. hardcoded in *.py files
#
%define	changeset_id ef3f08547688
#
Summary:	Pacemaker command line interface for management and configuration
Name:		crmsh
Version:	1.2.5
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://hg.savannah.gnu.org/hgweb/crmsh/archive/%{changeset_id}.tar.bz2
# Source0-md5:	e2276903e4174340d45de740de9c212c
Patch0:		%{name}-awk.patch
URL:		https://savannah.nongnu.org/projects/crmsh/
BuildRequires:	asciidoc
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cluster-glue-libs-devel
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
