#!/bin/bash
touch ip_banned.txt
sudo zgrep 'Ban ' /var/log/fail2ban.log* > ip_banned.txt
