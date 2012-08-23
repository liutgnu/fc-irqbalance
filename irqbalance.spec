Name:           irqbalance
Version:        1.0.3
Release:        6%{?dist}
Epoch:          2
Summary:        IRQ balancing daemon

Group:          System Environment/Base
License:        GPLv2
Url:            http://irqbalance.org/
Source0:        http://irqbalance.googlecode.com/files/irqbalance-%{version}.tar.gz
Source1:        irqbalance.sysconfig

BuildRequires:  autoconf automake libtool libcap-ng
BuildRequires:  glib2-devel pkgconfig libcap-ng-devel
%ifnarch %{arm}
BuildRequires:	numactl-devel numactl-libs
Requires: numactl-libs
%endif
Requires(post): systemd-units
Requires(postun):systemd-units
Requires(preun):systemd-units
#Requires(triggerun):systemd-units

ExclusiveArch: %{ix86} x86_64 ia64 ppc ppc64 %{arm}

Patch1: 0001-Add-sample-irqbalance-environment-file.patch
Patch2: 0002-introduce-banirq-option.patch
Patch3: 0003-When-IRQBALANCE_BANNED_CPUS-is-set-proc-stat-is-not-.patch
Patch4: 0004-Make-irqbalance-scan-for-new-irqs-when-it-detects-ne.patch
Patch5: 0005-Add-banscript-option.patch
Patch6: 0006-irqbalance-cpu-powersave-code-disabled-when-power_th.patch
Patch7: 0007-apply-affinity-hint-also-if-the-current-policy-is-su.patch
Patch8: 0008-irqlist-added-check-for-avoidance-of-division-by-zer.patch

%description
irqbalance is a daemon that evenly distributes IRQ load across
multiple CPUs for enhanced performance.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
%{configure}
CFLAGS="%{optflags}" make %{?_smp_mflags}

%install
install -D -p -m 0755 %{name} %{buildroot}%{_sbindir}/%{name}
install -D -p -m 0644 ./misc/irqbalance.service %{buildroot}/lib/systemd/system/irqbalance.service
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

install -d %{buildroot}%{_mandir}/man1/
install -p -m 0644 ./irqbalance.1 %{buildroot}%{_mandir}/man1/

%files
%defattr(-,root,root)
%doc COPYING AUTHORS
%{_sbindir}/irqbalance
/lib/systemd/system/irqbalance.service
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/sysconfig/irqbalance

%post
%systemd_post irqbalance.service

%preun
%systemd_preun irqbalance.service

%postun
%systemd_postun_with_restart irqbalance.service

%triggerun -- irqbalance < 2:0.56-3
if /sbin/chkconfig --level 3 irqbalance ; then
    /bin/systemctl enable irqbalance.service >/dev/null 2>&1 || :
fi
/sbin/chkconfig --del irqbalance >/dev/null 2>&1 || :

%changelog
* Wed Aug 22 2012 Petr Holasek <pholasek@redhat.com> - 2:1.0.3-5
- Make irqbalance scan for new irqs when it detects new irqs (bz832815)
- Fixes SIGFPE crash for some banning configuration (bz849792)
- Fixes affinity_hint values processing (bz832815)
- Adds banirq and bansript options (bz837049)
- imake isn't needed for building any more (bz844359)
- Fixes clogging of syslog (bz837646)
- Added IRQBALANCE_ARGS variable for passing arguments via systemd(bz837048)
- Fixes --hint-policy=subset behavior (bz844381)

* Sun Apr 15 2012 Petr Holasek <pholasek@redhat.com> - 2:1.0.3-4
- Updated libnuma dependencies

* Sun Feb  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2:1.0.3-3
- Build on ARM

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 02 2011 Neil Horman <nhorman@redhat.com> - 2:1.0.3-1
- Updated to latest upstream release

* Fri Nov 04 2011 Neil Horman <nhorman@redhat.com> - 2:1.0.2-1
- Updated to latest upstream release

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-4
- Rebuilt for glibc bug#747377

* Fri Oct 21 2011 Neil Horman <nhorman@redhat.com> - 2:1.0-3
- Fix another crash on non-numa systems (bz 748070)

* Mon Oct 17 2011 Neil Horman <nhorman@redhat.com> - 2:1.0-2
- Fix crash for systems with no numa node support

* Wed Oct 12 2011 Neil Horman <nhorman@redhat.com> - 2:1.0-1
- Update irqbalance to latest upstream version

* Fri May  6 2011 Bill Nottingham <notting@redhat.com> - 2:0.56-4
- fix upgrade trigger

* Fri Apr  8 2011 Peter Robinson <pbrobinson@gmail.com> - 2:0.56-3
- Fix build in rawhide
- Add license file to rpm
- Cleanup spec file

* Fri Mar 25 2011 Anton Arapov <anton@redhat.com> - 2:0.56-3
- rework init in order to respect systemd. (bz 659622)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jun 10 2010 Neil Horman <nhorman@redhat.com> - 2:0.56-1
- Updated to latest upstream version

* Wed Sep 09 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-25
- Fixing BuildRequires

* Fri Sep 04 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-24
- Fixing irqbalance initscript (bz 521246)

* Wed Sep 02 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-23
- Fixing BuildRequires for new config script

* Tue Sep 01 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-22
- Fixing BuildRequires for new config script

* Tue Sep 01 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-21
- Fixing BuildRequires for new config script

* Tue Sep 01 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-20
- Fixing BuildRequires for new config script

* Tue Sep 01 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-19
- Incorporate capng (bz 520699)

* Fri Jul 31 2009 Peter Lemenkov <lemenkov@gmail.com> - 2:0.55-18
- Added back accidentaly forgotten imake

* Fri Jul 31 2009 Peter Lemenkov <lemenkov@gmail.com> - 2:0.55-17
- Cosmetic fixes in spec-file
- Fixed rpmlint error in the init-script

* Tue Jul 28 2009 Peter Lemenkov <lemenkov@gmail.com> - 2:0.55-16
- Many imrovements in spec-file

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.55-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 6 2009 Neil Horman <nhorman@redhat.com>
- Update spec file to build for i586 as per new build guidelines (bz 488849)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.55-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Neil Norman <nhorman@redhat.com> - 2:0.55-12
- Remove odd Netorking dependence from irqbalance (bz 476179)

* Fri Aug 01 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:0.55-11
- fix license tag

* Tue Jun 04 2008 Neil Horman <nhorman@redhat.com> - 2:0.55-10
- Update man page to explain why irqbalance exits on single cache (bz 449949)

* Tue Mar 18 2008 Neil Horman <nhorman@redhat.com> - 2:0.55-9
- Rediff pid-file patch to not remove initial parse_cpu_tree (bz 433270)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2:0.55-8
- Autorebuild for GCC 4.3

* Thu Nov 01 2007 Neil Horman <nhorman@redhat.com> - 2:0.55-7
- Update to properly hadndle pid files (bz 355231)

* Thu Oct 04 2007 Neil Horman <nhorman@redhat.com> - 2:0.55-6
- Fix irqbalance init script (bz 317219)

* Fri Sep 28 2007 Neil Horman <nhorman@redhat.com> - 2:0.55-5
- Install pie patch
- Grab Ulis cpuparse cleanup (bz 310821)

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2:0.55-4
- Rebuild for selinux ppc32 issue.

* Thu Jul 05 2007 Neil Horman <nhorman@redhat.com> - 0.55.3
- Fixing LSB requirements (bz 246959)

* Tue Dec 12 2006 Neil Horman <nhorman@redhat.com> - 0.55-2
- Fixing typos in spec file (bz 219301)

* Tue Dec 12 2006 Neil Horman <nhorman@redhat.com> - 0.55-1
- Updating to version 0.55

* Mon Dec 11 2006 Neil Horman <nhorman@redhat.com> - 0.54-1
- Update irqbalance to new version released at www.irqbalance.org

* Wed Nov 15 2006 Neil Horman <nhorman@redhat.com> - 1.13-8
- Add ability to set default affinity mask (bz 211148)

* Wed Nov 08 2006 Neil Horman <nhorman@redhat.com> - 1.13-7
- fix up irqbalance to detect multicore (not ht) (bz 211183)

* Thu Nov 02 2006 Neil Horman <nhorman@redhat.com> - 1.13-6
- bumping up MAX_INTERRUPTS to support xen kernels
- rediffing patch1 and patch3 to remove fuzz

* Tue Oct 17 2006 Neil Horman <nhorman@redhat.com> - 1.13-5
- Making oneshot mean oneshot always (bz 211178)

* Wed Sep 13 2006 Peter Jones <pjones@redhat.com> - 1.13-4
- Fix subsystem locking

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 1.13-2
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)
- Remove hack to use cvs checkin ID as release as it doesn't follow
  packaging guidelines

* Tue Aug 01 2006 Neil Horman <nhorman@redhat.com>
- Change license to GPL in version 0.13

* Sat Jul 29 2006 Dave Jones <davej@redhat.com>
- identify a bunch more classes.

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

