#!/bin/bash

#This script will download, install, and configure Duo MFA for CentOS 7.x minimalservers
#Official instructions here https://duo.com/docs/duounix#install-pam_duo
#This is not complete yet. DO NOT USE

#install requirements
yum install -y wget openssl-devel pam-devel selinux-policy-devel
yum -y groupinstall "Development Tools"


#download latest Duo version
wget https://dl.duosecurity.com/duo_unix-latest.tar.gz

#extract downloaded tarball and change directory
mkdir /opt/duo_unix_latest || rm -r /opt/duo_unix_latest || mkdir /opt/duo_unix_latest
tar zxf duo_unix-latest.tar.gz -C /opt/duo_unix_latest

#build and install duo_unix with PAM support
/opt/duo_unix_latest/./configure --with-pam --prefix=/usr && make && sudo make -C /opt/duo_unix_latest install

#edit /etc/duo/pam_duo.conf with ikey, secret key, and hostname
#prompt user for input and add config below...

echo Enter the Duo integration key...
read ikey
echo Enter the Duo secret key...
read skey
echo Enter the Duo API hostname...
read $host

echo "[duo]" > /etc/duo/pam_duo.conf
echo "; Duo integration key" >> /etc/duo/pam_duo.conf
echo "ikey =" $ikey >> /etc/duo/pam_duo.conf
echo "; Duo secret key" >> /etc/duo/pam_duo.conf
echo "skey =" $skey >> /etc/duo/pam_duo.conf
echo "; Duo API host" >> /etc/duo/pam_duo.conf
echo "host =" $host >> /etc/duo/pam_duo.conf
echo "failmode = safe" >> /etc/duo/pam_duo.conf
echo "autopush = yes" >> /etc/duo/pam_duo.conf
echo "prompts = 1" >> /etc/duo/pam_duo.conf
echo "https_timeout=30" >> /etc/duo/pam_duo.conf

##This is where I need to pick up from next time I work on this
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.old
sudo cp duo_sshd_config /etc/ssh/sshd_config

sudo cp /etc/pam.d/sshd /etc/pam.d/sshd.old
sudo cp duo_pamd_sshd /etc/pam.d/sshd

sudo make -C /opt/duo_unix_latest/pam_duo semodule
sudo make -C /opt/duo_unix_latest/pam_duo semodule-install

sudo cp /etc/pam.d/system-auth /etc/pam.d/system-auth.old
sudo cp duo_pamd_system-auth /etc/pam.d/system-auth


