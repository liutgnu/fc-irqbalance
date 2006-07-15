Summary:        IRQ balancing daemon.
Name:           irqbalance
Version:        1.12
Release: 	%(R="$Revision$"; RR="${R##: }"; echo ${RR%%?})%{?dist}
Epoch:		1
Group:          System Environment/Base
License:        GPL/OSL
Source0:	irqbalance-0.12.tar.gz
Source1:	irqbalance.init
Source2:	irqbalance.sysconfig
Buildroot:      %{_tmppath}/%{name}-%{version}-root
Prereq:		/sbin/chkconfig /sbin/service
Patch1: irqbalance-pie.patch
Patch2: irqbalance-norebalance-zeroints.patch
ExclusiveArch:	i386 x86_64 ia64 ppc ppc64
Obsoletes:	kernel-utils

%description
irqbalance is a daemon that evenly distributes IRQ load across
multiple CPUs for enhanced performance.

%prep
%setup -q -c -a 0
%patch1 -p1
%patch2 -p1

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
* Fri Jul 14 2006 Jesse Keating <jkeating@redhat.com>
- rebuild

* Tue Jul 11 2006 Dave Jones <davej@redhat.com>
- Further lazy rebalancing tweaks.

* Sun Feb 26 2006 Dave Jones <davej@redhat.com>
- Don't rebalance IRQs where no interrupts have occured.

* Sun Feb 12 2006 Dave Jones <davej@redhat.com>
- Build for ppc[64] too.

* Thu Feb 09 2006 Dave Jones <davej@redhat.com>
- rebuild.

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- Rebuild with gcc4

* Tue Feb  8 2005 Dave Jones <davej@redhat.com>
- Build as pie, also -D_FORTIFY_SOURCE=2

* Tue Jan 11 2005 Dave Jones <davej@redhat.com>
- Add missing Obsoletes: kernel-utils.

* Mon Jan 10 2005 Dave Jones <davej@redhat.com>
- Start irqbalance in runlevel 2 too. (#102064)

* Sat Dec 18 2004 Dave Jones <davej@redhat.com>
- Initial packaging, based on kernel-utils.

