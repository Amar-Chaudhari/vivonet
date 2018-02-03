#!/bin/bash

echo "#### Installing Dependencies ####"
yum -y install epel-release
yum -y install make gcc openssl-devel autoconf automake rpm-build redhat-rpm-config python-devel openssl-devel kernel-devel kernel-debug-devel libtool wget vim

echo "#### Building OVS RPM ####"
mkdir -p ~/rpmbuild/SOURCES
wget http://openvswitch.org/releases/openvswitch-2.5.1.tar.gz
cp openvswitch-2.5.1.tar.gz ~/rpmbuild/SOURCES/
tar xfz openvswitch-2.5.1.tar.gz
sed 's/openvswitch-kmod, //g' openvswitch-2.5.1/rhel/openvswitch.spec > openvswitch-2.5.1/rhel/openvswitch_no_kmod.spec

rpmbuild -bb --nocheck ~/openvswitch-2.5.1/rhel/openvswitch_no_kmod.spec

echo "#### Installing OVS ####"
ls -l ~/rpmbuild/RPMS/x86_64/
yum -y localinstall ~/rpmbuild/RPMS/x86_64/openvswitch-2.5.1-1.x86_64.rpm

echo "#### Starting OVS ######"
systemctl start openvswitch.service
chkconfig openvswitch on
