%define underscore() %(echo %1 | sed 's/-/_/g')

Name: argo-probe-keycloak
Summary: Probe checking that keycloack login works.
Version: 0.1.0
Release: 1%{?dist}
Source0: %{name}-%{version}.tar.gz
License: ASL 2.0
Group: Network/Monitoring
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Prefix: %{_prefix}
BuildArch: noarch

BuildRequires: python3-devel
Requires: python36-requests


%description
This package includes probe that checks keycloak login.


%prep
%setup -q


%build
%{py3_build}


%install
%{py3_install "--record=INSTALLED_FILES" }


%clean
rm -rf $RPM_BUILD_ROOT


%files -f INSTALLED_FILES
%defattr(-,root,root,-)
%dir %{python3_sitelib}/%{underscore %{name}}/
%{python3_sitelib}/%{underscore %{name}}/*.py


%changelog
* Fri Jun 10 2022 Katarina Zailac <kzailac@gmail.com> - 0.1.0-1%{?dist}
- AO-650 Harmonize argo-mon probes
