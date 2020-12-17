# Analise_Openvpn_log
Script copies log file, analize last one week logs, find connection restarted and initiated times, creates file sorted by date and VPN client name and send email attached the files.

Warn: It is opensource

Used libraries: datetime, os, paramiko, dateutil, yaml, smtplib, pathlib, email

Note: Script is created for Pfsence #You can change some setting for Openvpn server

1. Creat your own credential file or encrypt-decrypting script. #For security reasons i cant share that script
2. When you call Backup_Log.py, it calls TextParser.py, and that calls Send_email.py
3. Additional notes are written in the codes.
