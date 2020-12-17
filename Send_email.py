import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from Hashing import decrypt #Calls Hashing.py for decrypting credentials

def mail_host():
    host = "mail.asb.az"
    return host


def if_error_occured (got_error, error):
    if got_error:
        #When error occur before log files is made ready

        send_to = ["rafail.sharifov@asb.az"]
        subject = "I got error"
        message =  'I got error below: \n' + error + """\n
         I need your help please
         This message was sent by python"""
        files = []
        
    else:
        # Everything is okay and i am going to send email to receivers


        send_to = ["rafail.sharifov@asb.az"]
        subject = "ATM weekly log"
        message = "This message was sent by avtomation tool created by Rafail"
        files = ["/root/log_files/Sorted_by_date.txt", "/root/log_files/Sorted_by_ATM.txt"]

    send_mail(send_to,subject, message, files)



try:
    def send_mail(send_to, subject, message, files): #Send email
        server = mail_host()
        port = 587
        use_tls = True
        credintials = decrypt(host_name=server)
        username = credintials[0]
        password = credintials[1]
        send_from = username
        """Compose and send email with provided info and attachments.
    
        Args:
            send_from (str): from name
            send_to (list[str]): to name(s)
            subject (str): message title
            message (str): message body
            files (list[str]): list of file paths to be attached to email
            server (str): mail server host name
            port (int): port number
            username (str): server auth username
            password (str): server auth password
            use_tls (bool): use TLS mode
        """

        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(message))

        for path in files:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(Path(path).name))
            msg.attach(part)

        smtp = smtplib.SMTP(server, port)
        if use_tls:
            smtp.starttls()
        smtp.login(username, password)
        smtp.sendmail(send_from, send_to, msg.as_string())
        print("I sent mail")
        smtp.quit()

except Exception as error: #Send mail when error occured
    got_error = True
    if_error_occured(got_error, error)
    print(error)


if __name__ == "__main__":
    if_error_occured(got_error=False, error='')