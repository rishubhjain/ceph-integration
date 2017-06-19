Name: tendrl-ceph-integration
Version: 1.4.2
Release: 1%{?dist}
BuildArch: noarch
Summary: Tendrl bridge for Ceph Storage
Source0: %{name}-%{version}.tar.gz
License: LGPLv2+
URL: https://github.com/Tendrl/ceph-integration

BuildRequires: python2-devel
BuildRequires: pytest
BuildRequires: systemd

Requires: python-msgpack
Requires: tendrl-commons

%description
Tendrl bridge for Ceph Storage

%prep
%setup

# Remove bundled egg-info
rm -rf %{name}.egg-info

%build
%{__python} setup.py build

%install
%{__python} setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
install -m  0755  --directory $RPM_BUILD_ROOT%{_sysconfdir}/tendrl/ceph-integration
install -m  0755 --directory $RPM_BUILD_ROOT%{_var}/log/tendrl/ceph-integration
install -m  0755  --directory $RPM_BUILD_ROOT%{_datadir}/tendrl/ceph-integration
install -Dm 0644  etc/tendrl/ceph-integration/ceph-integration.conf.yaml.sample $RPM_BUILD_ROOT%{_sysconfdir}/tendrl/ceph-integration/ceph-integration.conf.yaml
install -Dm 0644  etc/tendrl/ceph-integration/*.yaml.* $RPM_BUILD_ROOT%{_datadir}/tendrl/ceph-integration/.
install -Dm 0644 etc/tendrl/ceph-integration/logging.yaml.timedrotation.sample $RPM_BUILD_ROOT%{_sysconfdir}/tendrl/ceph-integration/ceph-integration_logging.yaml
install -p -D -m 0644 systemd/tendrl-ceph-integration.service $RPM_BUILD_ROOT%{_unitdir}/tendrl-ceph-integration.service

%post
systemctl enable tendrl-ceph-integration
%systemd_post tendrl-ceph-integration.service

%preun
%systemd_preun tendrl-ceph-integration.service

%postun
%systemd_postun_with_restart tendrl-ceph-integration.service

%check
py.test -v tendrl/ceph_integration/tests || :

%files -f INSTALLED_FILES
%dir %{_var}/log/tendrl/ceph-integration
%dir %{_sysconfdir}/tendrl/ceph-integration
%doc README.rst
%license LICENSE
%{_datadir}/tendrl/ceph-integration/.
%{_unitdir}/tendrl-ceph-integration.service
%{_sysconfdir}/tendrl/ceph-integration/ceph-integration_logging.yaml
%{_sysconfdir}/tendrl/ceph-integration/ceph-integration.conf.yaml

%changelog
* Mon Jun 19 2017 Rohan Kanade <rkanade@redhat.com> - 1.4.2-1
- Release tendrl-ceph-integration v1.4.2

* Thu Jun 08 2017 Rohan Kanade <rkanade@redhat.com> - 1.4.1-1
- Release tendrl-ceph-integration v1.4.1

* Fri Jun 02 2017 Rohan Kanade <rkanade@redhat.com> - 1.4.0-1
- Release tendrl-ceph-integration v1.4.0

* Thu May 18 2017 Rohan Kanade <rkanade@redhat.com> - 1.3.0-1
- Release tendrl-ceph-integration v1.3.0

* Tue Apr 18 2017 Rohan Kanade <rkanade@redhat.com> - 1.2.3-1
- Release tendrl-ceph-integration v1.2.3

* Sat Apr 01 2017 Rohan Kanade <rkanade@redhat.com> - 1.2.2-1
- Release tendrl-ceph-integration v1.2.2

* Mon Jan 23 2017 Timothy Asir Jeyasingh <tjeyasin@redhat.com> - 1.1-1
- Config file changes
- Import ceph

* Wed Oct 26 2016 Timothy Asir Jeyasingh <tjeyasin@redhat.com> - 0.0.1-1
- Initial build.
