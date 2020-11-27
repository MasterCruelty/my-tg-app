#!/bin/bash
sudo fail2ban-client status sshd | grep -A 15 Actions > ip_banned.txt