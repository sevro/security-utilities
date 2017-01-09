#!/bin/bash
#
# Install and configure a FTP server
#


# Install the software
if [ $(dpkg-query -W -f='${Status}' pure-ftpd 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
    echo "[*] Installing FTP server"
    apt-get install --yes --force-yes pure-ftpd;
    echo "[*] FTP server pure-ftpd installed"
else
    echo "[*] FTP server pure-ftpd already installed"
fi

echo "[*] Adding system group 'ftpgroup' and system user 'ftpuser'"
groupadd ftpgroup
useradd -g ftpgroup -d /dev/null -s /etc ftpuser


echo "[*] Adding virtual user 'datenstrom'"
pure-pw useradd datenstrom -u ftpuser -d /ftphome


echo "[*] Creating and configuring database"
pure-pw mkdb
cd /etc/pure-ftpd/auth/
ln -s ../conf/PureDB 60pdb


echo "[*] Setting up directories"
mkdir -p /ftphome
chown -R ftpuser:ftpgroup /ftphome/


echo "[*] Restarting pure-ftpd service"
/etc/init.d/pure-ftpd restart


echo "[*] Done!"
exit 0
