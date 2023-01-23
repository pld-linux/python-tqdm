# TODO: bash-completion with tqdm/completion.sh
#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Fast, Extensible Progress Meter
Summary(pl.UTF-8):	Szybki, rozszerzalny wskaźnik postępu
Name:		python-tqdm
Version:	4.64.1
Release:	1
License:	MPL v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/tqdm/
Source0:	https://files.pythonhosted.org/packages/source/t/tqdm/tqdm-%{version}.tar.gz
# Source0-md5:	5822af464d77ea156ad1167c23e1bdac
URL:		https://pypi.org/project/tqdm/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 1:42
BuildRequires:	python-setuptools_scm >= 3.4
BuildRequires:	python-toml
%if %{with tests}
BuildRequires:	python-pytest
BuildRequires:	python-pytest-timeout
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools >= 1:42
BuildRequires:	python3-setuptools_scm >= 3.4
BuildRequires:	python3-toml
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-asyncio
BuildRequires:	python3-pytest-timeout
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Fast, Extensible Progress Meter.

%description -l pl.UTF-8
Szybki, rozszerzalny wskaźnik postępu.

%package -n python3-tqdm
Summary:	Fast, Extensible Progress Meter
Summary(pl.UTF-8):	Szybki, rozszerzalny wskaźnik postępu
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-tqdm
Fast, Extensible Progress Meter.

%description -n python3-tqdm -l pl.UTF-8
Szybki, rozszerzalny wskaźnik postępu.

%prep
%setup -q -n tqdm-%{version}

# only py3
%{__sed} -i -e 's/--asyncio-mode=strict//; s/--durations-min=[.0-9]*//' setup.cfg

# fail in collection stage with unexpected version of ipython tools installed
%{__rm} tests/tests_notebook.py

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_timeout" \
%{__python} -m pytest tests -k 'not perf and not test_pandas'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_asyncio.plugin,pytest_timeout" \
%{__python3} -m pytest tests -k 'not perf and not tests_asyncio and not test_pandas' --asyncio-mode=strict --durations-min=0.1
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

%{__mv} $RPM_BUILD_ROOT%{_bindir}/tqdm{,-2}
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/tqdm/completion.sh

install -d $RPM_BUILD_ROOT%{_examplesdir}
cp -pr examples $RPM_BUILD_ROOT%{_examplesdir}/python-tqdm-%{version}
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/tqdm{,-3}
ln -sf tqdm-3 $RPM_BUILD_ROOT%{_bindir}/tqdm
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/tqdm/completion.sh

install -d $RPM_BUILD_ROOT%{_examplesdir}
cp -pr examples $RPM_BUILD_ROOT%{_examplesdir}/python3-tqdm-%{version}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENCE README.rst
%attr(755,root,root) %{_bindir}/tqdm-2
%{py_sitescriptdir}/tqdm
%{py_sitescriptdir}/tqdm-%{version}-py*.egg-info
%{_examplesdir}/python-tqdm-%{version}
%endif

%if %{with python3}
%files -n python3-tqdm
%defattr(644,root,root,755)
%doc LICENCE README.rst
%attr(755,root,root) %{_bindir}/tqdm
%attr(755,root,root) %{_bindir}/tqdm-3
%{py3_sitescriptdir}/tqdm
%{py3_sitescriptdir}/tqdm-%{version}-py*.egg-info
%{_examplesdir}/python3-tqdm-%{version}
%endif
