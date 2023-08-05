
%define with_python3 0
%if 0%{?fedora}
%define with_python3 1
%endif

Summary: The libvirt virtualization API python2 binding
Name: libvirt-python
Version: 3.10.0
Release: 1%{?dist}%{?extra_release}
Source0: http://libvirt.org/sources/python/%{name}-%{version}.tar.gz
Url: http://libvirt.org
License: LGPLv2+
Group: Development/Libraries
BuildRequires: libvirt-devel >= 0.9.11
BuildRequires: python-devel
BuildRequires: python-nose
BuildRequires: python-lxml
%if %{with_python3}
BuildRequires: python3-devel
BuildRequires: python3-nose
BuildRequires: python3-lxml
%endif

# Don't want provides for python shared objects
%{?filter_provides_in: %filter_provides_in %{python_sitearch}/.*\.so}
%{?filter_setup}

%description
The libvirt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libvirt library to use the virtualization capabilities
of recent versions of Linux (and other OSes).

%package -n python2-libvirt
Summary: The libvirt virtualization API python2 binding
Url: http://libvirt.org
License: LGPLv2+
Group: Development/Libraries
%{?python_provide:%python_provide python2-libvirt}
Provides: libvirt-python = %{version}-%{release}
Obsoletes: libvirt-python <= 3.6.0-1%{?dist}

%description -n python2-libvirt
The python2-libvirt package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libvirt library to use the virtualization capabilities
of recent versions of Linux (and other OSes).

%if %{with_python3}
%package -n python3-libvirt
Summary: The libvirt virtualization API python3 binding
Url: http://libvirt.org
License: LGPLv2+
Group: Development/Libraries
%{?python_provide:%python_provide python3-libvirt}
Provides: libvirt-python3 = %{version}-%{release}
Obsoletes: libvirt-python3 <= 3.6.0-1%{?dist}

%description -n python3-libvirt
The python3-libvirt package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libvirt library to use the virtualization capabilities
of recent versions of Linux (and other OSes).
%endif

%prep
%setup -q

# Unset execute bit for example scripts; it can introduce spurious
# RPM dependencies, like /usr/bin/python which can pull in python2
# for the -python3 package
find examples -type f -exec chmod 0644 \{\} \;

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
%if %{with_python3}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
%endif

%install
%{__python} setup.py install --skip-build --root=%{buildroot}
%if %{with_python3}
%{__python3} setup.py install --skip-build --root=%{buildroot}
%endif

%check
%{__python} setup.py test
%if %{with_python3}
%{__python3} setup.py test
%endif

%files -n python2-libvirt
%defattr(-,root,root)
%doc ChangeLog AUTHORS NEWS README COPYING COPYING.LESSER examples/
%{_libdir}/python2*/site-packages/libvirt.py*
%{_libdir}/python2*/site-packages/libvirt_qemu.py*
%{_libdir}/python2*/site-packages/libvirt_lxc.py*
%{_libdir}/python2*/site-packages/libvirtmod*
%{_libdir}/python2*/site-packages/*egg-info

%if %{with_python3}
%files -n python3-libvirt
%defattr(-,root,root)
%doc ChangeLog AUTHORS NEWS README COPYING COPYING.LESSER examples/
%{_libdir}/python3*/site-packages/libvirt.py*
%{_libdir}/python3*/site-packages/libvirtaio.py*
%{_libdir}/python3*/site-packages/libvirt_qemu.py*
%{_libdir}/python3*/site-packages/libvirt_lxc.py*
%{_libdir}/python3*/site-packages/__pycache__/libvirt.cpython-*.py*
%{_libdir}/python3*/site-packages/__pycache__/libvirt_qemu.cpython-*.py*
%{_libdir}/python3*/site-packages/__pycache__/libvirt_lxc.cpython-*.py*
%{_libdir}/python3*/site-packages/__pycache__/libvirtaio.cpython-*.py*
%{_libdir}/python3*/site-packages/libvirtmod*
%{_libdir}/python3*/site-packages/*egg-info
%endif

%changelog
