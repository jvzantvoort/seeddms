%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global srcname seeddms
%global srcversion 0.0.1

Name:           python-seeddms
Version:        0.0.2
Release:        1%{?dist}
Summary:        An interface to seeddms REST API

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/jvzantvoort/seeddms
Source0:        %{srcname}-%{srcversion}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools python-sphinx
Requires:       python-werkzeug

Requires:       python2-requests
# BuildRequires:  python-jinja2

%description
TBD

%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation and examples for %{name}.

%prep
%setup -q -n %{srcname}-%{srcversion}
## %{__sed} -i "/platforms/ a\    requires=['Jinja2 (>=2.4)']," setup.py

%build
%{__python} setup.py build

pushd docs
make html
popd

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%check
#{__python} setup.py test

#if 0%{?with_python3}
#pushd %{py3dir}
#{__python3} setup.py test
#popd
#endif


%files
%doc LICENSE README.md
%{python_sitelib}/*.egg-info
# %{python_sitelib}/*.egg-link
%{python_sitelib}/seeddms

%files doc
%doc docs/build/html

%changelog
* Thu Jul 19 2018 John van Zantvoort <john@vanzantvoort.org> 0.0.2-1
- new package built with tito


