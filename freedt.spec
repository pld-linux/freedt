Summary:	freedt - a reimplementation of Dan Bernstein's daemontools
Summary(pl.UTF-8):	freedt - reimplementacja daemontools Dana Bernsteina
Name:		freedt
Version:	0.21
Release:	1
License:	GPL
Group:		Networking/Admin
Source0:	http://offog.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	28484635b0e149d00b872b6b0d935683
Source2:	%{name}.sysconfig
Source3:	%{name}.init
URL:		http://offog.org/code/freedt.html
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	rc-scripts
Requires(post,preun):	/sbin/chkconfig
Obsoletes:	daemontools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
freedt currently includes feature-equivalent replacements for argv0,
envdir, envuidgid, setlock, setuidgid, softlimit, supervise, svc,
svok, svscan, svstat and recordio. It also includes dumblog (a simple
multilog replacement), mkservice (a script for automatically creating
service directories), anonidentd (an anonimising identd
implementation) and ratelimit (a bandwidth-limiting filter along the
lines of recordio).

%description -l pl.UTF-8
freedt aktualnie zawiera funkcjonalnie równoważne zamienniki argv0,
envdir, envuidgid, setlock, setuidgid, softlimit, supervise, svc,
svok, svscan, svstat i recordio. Zawiera również dumblog (prosty
zamiennik multiloga), mkservice (skrypt do automatycznego tworzenia
katalogów dla usług), anonidentd (zapewniającą anonimowość
implementację identd) oraz ratelimit (filtr ograniczający pasmo
działający w recordio).

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
%service svscan restart

%preun
if [ "$1" = "0" ]; then
	%service svscan stop
	/sbin/chkconfig --del svscan
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/*
%attr(700,root,root) /var/lib/service
%attr(754,root,root) /etc/rc.d/init.d/svscan
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/svscan
