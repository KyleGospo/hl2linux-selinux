%global selinuxtype	targeted
%global moduletype	services
%global modulenames	hl2linux
%global _format() export %1=""; for x in %{modulenames}; do %1+=%2; %1+=" "; done;
%global relabel_files() \ # ADD files in *.fc file
%global selinux_policyver 37.19-1.fc37

# Package information
Name:			hl2linux-selinux
Version:		1.1
Release:		1%{?dist}
License:		GPLv2
Group:			System Environment/Base
Summary:		SELinux policy for hl2_linux (Team Fortress 2)
BuildArch:		noarch
URL:			https://github.com/KyleGospo/hl2linux-selinux
Requires(post):	selinux-policy-base >= %{selinux_policyver}, selinux-policy-targeted >= %{selinux_policyver}, policycoreutils, libselinux-utils
BuildRequires:	selinux-policy selinux-policy-devel

Source:			{{{ git_dir_pack }}}

%description
SELinux policy for use with hl2_linux (Team Fortress 2). Resolves issues with missing in-game audio.

%prep
{{{ git_dir_setup_macro }}}

%build
make SHARE="%{_datadir}" TARGETS="%{modulenames}"

%install
%_format MODULES $x.pp.bz2
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 0644 $MODULES \
	%{buildroot}%{_datadir}/selinux/packages

%post
%_format MODULES %{_datadir}/selinux/packages/$x.pp.bz2
%{_sbindir}/semodule -n -s %{selinuxtype} -i $MODULES
if %{_sbindir}/selinuxenabled ; then
    %{_sbindir}/load_policy
    %relabel_files
fi


%postun
if [ $1 -eq 0 ]; then
	%{_sbindir}/semodule -n -r %{modulenames} &> /dev/null || :
	if %{_sbindir}/selinuxenabled ; then
		%{_sbindir}/load_policy
		%relabel_files
	fi
fi

%files
%license LICENSE
%doc README.md
%defattr(-,root,root,0755)
%attr(0644,root,root) %{_datadir}/selinux/packages/*.pp.bz2

%changelog
* Sat Mar 04 2023 Kyle Gospodnetich <me@kylegospodneti.ch> - 1.0-1
- First Build
