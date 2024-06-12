%global pack syncstar
%global desc Guest operated service for creating bootable USB storage devices at any community conference kiosk

Name:           %{pack}
Version:        0.1.0a2
Release:        1%{?dist}
Summary:        %{desc}

License:        AGPL-3.0-or-later
Url:            https://github.com/gridhead/%{pack}
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel

Requires:       coreutils
Requires:       util-linux
Requires:       redis

%description
%{desc}

%prep
%autosetup -n %{pack}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pack}

%files -f %{pyproject_files}
%doc README.md
%license LICENSE
%{_bindir}/%{name}

%changelog

* Wed Jun 12 2024 Akashdeep Dhar <t0xic0der@fedoraproject.org> - 0.1.0a1-1
- Add task management module for the service
- Format the codebase using Ruff
- Initialize the project codebase
- Add preliminary code quality checks
- Fix `TemplateNotFound` errors by replacing absolute paths with relative ones
- Set up the project documentation
- Utilize icons to make the frontend more accessible
- Add service units for SyncStar endpoint and worker
- Show available images archive on dashboard with font changes
- Per-type organization in documentation and frontend
- Add dependencies for mocking functionalities
- Change test configuration for coverage support
- Add testing client for endpoint testing
- Add testcases for the authentication middleware
- Add testcases for the home endpoint
- Add testcases for the enroll endpoint
- Add testcases for the checking endpoint
- Add testcases for the scanning endpoint
- Include static assets for testing purposes
- Add testcases for base utilities
- Add testcases for images configuration utilities
- Add testcases for standard configuration utilities
- Add testcases for command line interface
- Add testcases for greeting utilities
- Add testcases for worker utilities
- Include helper modules for testing
- Complete the saga of including testcases
- Make subtle cosmetic changes to the list subtitle
- Add type hints for a couple of missed out functions
- Format the spacing between the spacing and imports
- Create a restore point to get back to after tests are done
- Add screenshots of the project frontend
- Change licensing from `GPL-3.0-or-later` to `AGPL-3.0-or-later`
