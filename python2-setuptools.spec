%global srcname setuptools
 
Name:           python2-%{srcname}
Version:        40.8.0
Release:        1%{?dist}
Summary:        Easily download, build, install, upgrade, and uninstall Python packages
 
License:        PSF
URL:            https://pypi.org/project/setuptools/
Source0:        https://github.com/pypa/setuptools/archive/v%{version}.tar.gz
BuildRequires:  python2 python2-devel 
BuildRequires:  python2-pip 
BuildRequires:  python2-six 
BuildRequires:  python2-appdirs 
BuildRequires:  python2-packaging 
BuildRequires:  python2-pytest
BuildArch:      noarch
%{?python_provide:%python_provide python2-%{srcname}} 
Recommends:	python2-appdirs
Recommends:	python2-packaging
 
%description
Easily download, build, install, upgrade, and uninstall Python packages
 
%prep
%autosetup -n %{srcname}-%{version}

  rm -r $PWD/{pkg_resources,setuptools}/{extern,_vendor}

  # Upstream devendoring logic is badly broken, see:
  # https://bugs.archlinux.org/task/58670
  # https://github.com/pypa/pip/issues/5429
  # https://github.com/pypa/setuptools/issues/1383
  # The simplest fix is to simply rewrite import paths to use the canonical
  # location in the first place
  for _module in setuptools pkg_resources '' ; do
      find $PWD/$_module -name \*.py -exec sed -i \
          -e 's/from '$_module.extern' import/import/' \
          -e 's/from '$_module.extern'./from /' \
          -e 's/import '$_module.extern'./import /' \
          -e "s/__import__('$_module.extern./__import__('/" \
          {} +
    done

  # Remove post-release tag since we are using stable tags
  sed -e '/tag_build = .post/d' \
      -e '/tag_date = 1/d' \
      -i $PWD/setup.cfg

  # 'Clean' installation is expected to fail since we removed bundled packages
  sed -i '/^def test_clean_env_install/i import pytest\n\n@pytest.mark.xfail' $PWD/setuptools/tests/test_virtualenv.py

  # Tests failed. Importing an unbundled new setuptools in a virtualenv does not work, but this won't
  # affect normal virtualenv usage (which don't have to import the unbundled setuptools in *current*
  # dir.
  sed -e '/^def test_pip_upgrade_from_source/i @pytest.mark.xfail' \
      -e '/^def test_test_command_install_requirements/i @pytest.mark.xfail' \
      -e '/^def test_no_missing_dependencies/i @pytest.mark.xfail' \
      -i $PWD/setuptools/tests/test_virtualenv.py

  sed -i -e "s|^#\!.*/usr/bin/env python|#!/usr/bin/python2|" setuptools/command/easy_install.py
 
%build
/usr/bin/python2 bootstrap.py
/usr/bin/python2 setup.py build
 
%install

  # https://github.com/pypa/setuptools/pull/810
  export PYTHONDONTWRITEBYTECODE=1

/usr/bin/python2 setup.py install --prefix=/usr --root=%{buildroot} --optimize=1 --skip-build
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

* Tue Feb 19 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 40.8.0-1
- Upstream
