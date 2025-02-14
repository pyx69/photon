Summary:        Heapster enables Container Cluster Monitoring and Performance Analysis.
Name:           heapster
Version:        1.5.4
Release:        7%{?dist}
License:        Apache 2.0
URL:            https://github.com/wavefrontHQ/cadvisor
Source0:        https://github.com/kubernetes/heapster/archive/%{name}-%{version}.tar.gz
%define sha512  heapster=9c5f1e11b224efe6aaa42aad0daecede2c22d86d692a9d008643d9731d78becce98c8332ebe8d17568a93abe1f56dabf868dcd7ebc1e7b48e1f6f6f8f3878152
Patch0:         go-27704.patch
Patch1:         go-27842.patch
%if %{with_check}
Patch2:         make-check-failure.patch
%endif
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go
BuildRequires:  unzip

%description
Heapster collects and interprets various signals like compute resource usage, lifecycle events, etc, and exports cluster metrics via REST endpoints.

%prep
# Using autosetup is not feasible
%setup -q

pushd vendor/golang.org/x/net
%patch0 -p1
%patch1 -p1
popd
%if %{with_check}
%patch2 -p1
%endif

%build
export GO111MODULE=auto
mkdir -p $GOPATH/src/k8s.io/heapster
cp -r . $GOPATH/src/k8s.io/heapster
cd $GOPATH/src/k8s.io/heapster
%make_build

%install
cd $GOPATH/src/k8s.io/heapster
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 heapster %{buildroot}%{_bindir}
install -p -m 0755 eventer %{buildroot}%{_bindir}

%check
cd $GOPATH/src/k8s.io/heapster
make test-unit %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/heapster
%{_bindir}/eventer

%changelog
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.4-7
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 1.5.4-6
- Bump up version to compile with new go
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.5.4-5
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.5.4-4
- Bump up version to compile with new go
* Mon Nov 16 2020 Prashant S Chauhan <psinghchauha@vmware.com> 1.5.4-3
- Fix make check
* Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 1.5.4-2
- Fix CVE-2018-17846 and CVE-2018-17143
* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 1.5.4-1
- Update to version 1.5.4
* Thu Aug 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.2-1
- Initial heapster package
