#!/bin/bash

#This script will download, install, and configure Duo MFA for CentOS 7.x servers
#Official instructions here

#install requirements
yum install -y openssl-devel pam-devel selinux-policy-devel

#download latest Duo version
wget https://dl.duosecurity.com/duo_unix-latest.tar.gz.

#extract downloaded tarball and change directory
mkdir duo_unix_latest && tar zxf duo_unix-latest.tar.gz -C duo_unix_latest --strip-components 1
cd duo_unix_latest
