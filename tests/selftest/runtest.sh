#!/bin/bash
# vim: dict=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /CoreOS/rng-tools/Sanity/selftest
#   Description: Executes the upstream test suite comming with the package
#   Author: Miroslav Vadkerti <mvadkert@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2010 Red Hat, Inc. All rights reserved.
#
#   This copyrighted material is made available to anyone wishing
#   to use, modify, copy, or redistribute it subject to the terms
#   and conditions of the GNU General Public License version 2.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE. See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public
#   License along with this program; if not, write to the Free
#   Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301, USA.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Include rhts environment
. /usr/bin/rhts-environment.sh || exit 1
. /usr/share/beakerlib/beakerlib.sh || exit 1

PACKAGE="irqbalance"
PACKAGES="irqbalance automake autoconf libtool libcap-ng-devel glib2-devel pkgconf systemd ncurses-devel numactl-devel"
UPSTREAMPKG="irqbalance-*"
BUILDLOG=`mktemp`
TESTLOG=`mktemp`
TARGET=$(echo `uname -m` | egrep ppc)
if [[ $TARGET != "" ]]; then TARGET="--target `uname -m`"; fi
TOPDIR=`mktemp -d`
SPEC="$TOPDIR/SPECS/$PACKAGE*.spec"
TESTDIR="$TOPDIR/BUILD/$UPSTREAMPKG/"

rlJournalStart
    rlPhaseStartSetup
    	for PKG in $PACKAGES; do
	        rlAssertRpm $PKG
	done
    rlPhaseEnd
    rlPhaseStartTest
	rlFetchSrcForInstalled $PACKAGE
	rlRun "rpm -ivh --define '_topdir $TOPDIR' $PACKAGE*.src.rpm" 0 "Installing $PACKAGE src rpm"
	echo "+ Building $PACKAGE (Log: $BUILDLOG)"
	echo "+ Build command: rpmbuild -bc $SPEC $TARGET"
	rlRun "rpmbuild --define '_topdir $TOPDIR' -bc $SPEC $TARGET &> $BUILDLOG"
	echo "+ Buildlog:"
	tail -n 100 $BUILDLOG
	rlRun "pushd ."
 	rlRun "cd $TESTDIR"
	rlRun "make check &> $TESTLOG"   
	if [ $? -eq 0 ]
	then
		rlPass "Selftest Passed"
	else
		rlFail "Selftest Failed"
	fi
    rlPhaseEnd

    rlPhaseStartCleanup
    	rlRun "popd"
	rlRun "rm -rf $PACKAGE*.src.rpm" 0 "Removing source rpm"    
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
