%global pack syncstar

Name:           %{pack}
Version:        0.1.0a4
Release:        1%{?dist}
Summary:        Service for creating bootable USB storage devices at community conference kiosks

# The syncstar project is licensed under AGPL-3.0-or-later license, except for the following files
#
# MIT license -
# syncstar/frontend/static/css3/bs.min.css
# syncstar/frontend/static/jscn/bs.min.js

License:        AGPL-3.0-or-later AND MIT
Url:            https://github.com/gridhead/%{pack}
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel

Requires:       coreutils
Requires:       util-linux
Requires:       redis

%description
SyncStar lets users create bootable USB storage devices with the operating
system image of their choice. This application is intended to be deployed on
kiosk devices and electronic signages where conference guests and booth
visitors can avail its services.

%prep
%autosetup -n %{pack}-%{version}

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pack}

%check
%tox

%files -f %{pyproject_files}
%doc README.md
%license LICENSE
%{_bindir}/%{name}

%changelog

* Sat Jun 22 2024 Akashdeep Dhar <t0xic0der@fedoraproject.org> - 0.1.0a4-1
- Initial release for SyncStar project
- More information can be found on https://github.com/gridhead/syncstar/releases/tag/0.1.0

