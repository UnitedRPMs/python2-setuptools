%global srcname setuptools
 
Name:           python2-%{srcname}
Version:        44.1.1
Release:        1%{?dist}
Summary:        Easily download, build, install, upgrade, and uninstall Python packages
 
License:        PSF
URL:            https://pypi.org/project/setuptools/
Source0:        https://github.com/pypa/setuptools/archive/v%{version}.tar.gz
BuildRequires:  python2.7  git
#BuildRequires:  python2-pip 
#BuildRequires:  python2-six 
#BuildRequires:  python2-appdirs 
#BuildRequires:  python2-packaging 
#BuildRequires:  python2-pytest
BuildArch:      noarch
%{?python_provide:%python_provide python2-%{srcname}} 
Recommends:	python2-appdirs
Recommends:	python2-packaging
 
%description
Easily download, build, install, upgrade, and uninstall Python packages
 
%prep
%autosetup -n %{srcname}-%{version}

  sed -i -e "s|^#\!.*/usr/bin/env python|#!/usr/bin/python2|" setuptools/command/easy_install.py
 
%build
python2 bootstrap.py
%install

python2 setup.py install --root %{buildroot} --optimize=1
#/usr/bin/python2 setup.py install --prefix=/usr --root=%{buildroot} --optimize=1 --skip-build
rm -f %{buildroot}/usr/bin/easy_install
 
%files 
%{_bindir}/easy_install-2.7
%{python2_sitelib}/easy_install.py
%{python2_sitelib}/easy_install.pyc
%{python2_sitelib}/easy_install.pyo
%{python2_sitelib}/pkg_resources/
%{python2_sitelib}/setuptools-*.egg-info/
%{python2_sitelib}/setuptools/
 
%changelog

* Sat Apr 30 2022 Unitedrpms Project <unitedrpms AT protonmail DOT com> 44.1.1-1
- Updated to 44.1.1

* Tue Feb 19 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 40.8.0-1
- Upstream
