Summary:	freedt - a reimplementation of Dan Bernstein's daemontools
Summary[p]:	freedt - reimplementacja daemontools Dana Bernsteina
Name:		freedt
Version:	0.18
Release:	1
License:	GPL
Group:		Networking/Admin
Source0:	http://offog.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	7751ecf870b58cb5d3725ca209339fe6
Source2:	%{name}.sysconfig
Source3:	%{name}.init
URL:		http://offog.org/code/freedt.html
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
freedt currently includes feature-equivalent replacements for argv0,
envdir, envuidgid, setlock, setuidgid, softlimit, supervise, svc,
svok, svscan, svstat and recordio. It also includes dumblog (a simple
multilog replacement), mkservice (a script for automatically creating
service directories), anonidentd (an anonimising identd
implementation) and ratelimit (a bandwidth-limiting filter along the
lines of recordio).

%description -l pl
freedt aktualnie zawiera funkcjonalnie równowa¿ne zamienniki argv0,
envdir, envuidgid, setlock, setuidgid, softlimit, supervise, svc,
svok, svscan, svstat i recordio. Zawiera równie¿ dumblog (prosty
zamiennik multiloga), mkservice (skrypt do automatycznego tworzenia
katalogów dla us³ug), anonidentd (zapewniaj±c± anonimowo¶æ
implementacjê identd) oraz ratelimit (filtr ograniczaj±cy pasmo
wzd³u¿(???) linii recordio).

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT/var/lib/service

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/svscan
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/svscan

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add svscan
if [ -f /var/lock/subsys/svscan ]; then
	/etc/rc.d/init.d/svscan restart >&2
else
	echo "Execute \"/etc/rc.d/init.d/svscan start\" to start svscan daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/svscan ]; then
		/etc/rc.d/init.d/svscan stop >&2
	fi
	/sbin/chkconfig --del svscan
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/*
%attr(700,root,root) /var/lib/service
%attr(754,root,root) /etc/rc.d/init.d/svscan
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/svscan
