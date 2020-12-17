import os
import paramiko
from Send_email import if_error_occured #Send_email.py is another script file that sends email
from Hashing import decrypt #Hashing is another Hashing.py file that encrypt and decrypt passwords. For security reasons i cant attach here.

host_name = "10.124.49.12"


try:
    def ssh_connect(host_name): #Connecting to host_name server to backup log file
        credentials = decrypt(host_name) #decrrypt() is another define function that is under "Hashing.py" file. For secutiry reasons i cant attach that file here.
        username = credentials[0]
        password = credentials[1]


        localpath = "/root/log_files/openvpn.log"
        remotepath = "/var/log/openvpn.log"

        ssh = paramiko.SSHClient()
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname = host_name, username=username, password=password)
        sftp = ssh.open_sftp()
        sftp.get(remotepath, localpath)
        sftp.close()
        ssh.close()

        from TextParser import parse_file
        parse_file()


    if __name__ == "__main__": #When Backup_Log.py called, runs ssh_connect() define
        ssh_connect(host_name)


except Exception as error:
    #If error happens in code above, script calls if_error_occured define and that sends email to me
    got_error = True
    if_error_occured(got_error, error)
