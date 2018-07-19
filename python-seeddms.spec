%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global srcname seeddms

Name:           python-seeddms
Version:        0.0.2
Release:        4
Summary:        Python library to access the SeedDMS REST API

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/jvzantvoort/seeddms
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools python-sphinx
Requires:       python2-requests

%description

Python library to access the SeedDMS REST API.

%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation and examples for %{name}.

%prep
%setup -q -n %{name}-%{version}

%build
%{__python} setup.py build

pushd docs
make html
popd

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%doc LICENSE README.md
%{python_sitelib}/*.egg-info
# %{python_sitelib}/*.egg-link
%{python_sitelib}/seeddms

%files doc
%doc docs/build/html

%changelog
* Thu Jul 19 2018 John van Zantvoort <john@vanzantvoort.org> 0.0.2-4
- updated specfile some more (john@vanzantvoort.org)

* Thu Jul 19 2018 John van Zantvoort <john@vanzantvoort.org> 0.0.2-3
- more fidling with spec (john@vanzantvoort.org)

* Thu Jul 19 2018 John van Zantvoort <john@vanzantvoort.org> 0.0.2-2
- minor fix on specfile (john@vanzantvoort.org)

* Thu Jul 19 2018 John van Zantvoort <john@vanzantvoort.org>
- minor fix on specfile (john@vanzantvoort.org)

* Thu Jul 19 2018 John van Zantvoort <john@vanzantvoort.org> 0.0.2-1
- new package built with tito


