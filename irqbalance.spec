Summary:        IRQ balancing daemon.
Name:           irqbalance
Version:        1.12
Release: 	%(R="$Revision$"; RR="${R##: }"; echo ${RR%%?})
Epoch:		1
Group:          System Environment/Base
License:        GPL/OSL
Source0:	irqbalance-0.12.tar.gz
Source1:	irqbalance.init
Source2:	irqbalance.sysconfig
Buildroot:      %{_tmppath}/%{name}-%{version}-root
Prereq:		/sbin/chkconfig /sbin/service
Patch1: irqbalance-pie.patch
ExclusiveArch:	i386 x86_64 ia64
Obsoletes:	kernel-utils

%description
irqbalance is a daemon that evenly distributes IRQ load across
multiple CPUs for enhanced performance.

%prep
%setup -q -c -a 0
%patch1 -p1

%build
rm -rf $RPM_BUILD_ROOT

mkdir -p %{buildroot}/usr/sbin
mkdir -p %{buildroot}/usr/man
mkdir -p %{buildroot}/etc/rc.d/init.d
mkdir -p %{buildroot}/etc/sysconfig

cd irqbalance
make CFLAGS="$RPM_OPT_FLAGS -fpie -pie"

%install
mkdir -p %{buildroot}/usr/share/man/man{1,8}

cd irqbalance
install irqbalance  %{buildroot}/usr/sbin
install %{SOURCE1} %{buildroot}/etc/rc.d/init.d/irqbalance
install %{SOURCE2} %{buildroot}/etc/sysconfig/irqbalance
install irqbalance.1 %{buildroot}/usr/share/man/man1/

chmod -R a-s %{buildroot}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && [ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT;

%files
%defattr(-,root,root)
/usr/sbin/irqbalance
%attr(0644,root,root) %{_mandir}/*/*
/etc/rc.d/init.d/irqbalance
%attr(0644,root,root) /etc/sysconfig/irqbalance

%preun
if [ "$1" = "0" ] ; then
 /sbin/chkconfig --del irqbalance
fi

%post
/sbin/chkconfig --add irqbalance

%triggerpostun -- kernel-utils
/sbin/chkconfig --add irqbalance
exit 0


%changelog
* Tue Feb  8 2005 Dave Jones <davej@redhat.com>
- Build as pie, also -D_FORTIFY_SOURCE=2

* Tue Jan 11 2005 Dave Jones <davej@redhat.com>
- Add missing Obsoletes: kernel-utils.

* Mon Jan 10 2005 Dave Jones <davej@redhat.com>
- Start irqbalance in runlevel 2 too. (#102064)

* Sat Dec 18 2004 Dave Jones <davej@redhat.com>
- Initial packaging, based on kernel-utils.

