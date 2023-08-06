if __name__ == "__main__":
    import sys
    sys.path.append("..")

import os
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email import encoders

__all__ = 'img_sendmail', 'img_sendmail_internal'

def formatted_address(address):
    return address if isinstance(address, basestring) else formataddr(address)

def create_message(sender, recipients, cc_recipients, subject):
    message = MIMEMultipart()
    message["To"] = ", ".join(formatted_address(address) for address in recipients)
    message["From"] = formatted_address(sender)
    message["Reply-To"] = formatted_address(sender)
    if cc_recipients:
        message["Cc"] = ", ".join(formatted_address(address) for address in cc_recipients)
    message["Subject"] = subject
    return message

def attach_message(message, content):
    if isinstance(content, tuple):
        plain, html = content
        attachment = MIMEMultipart('alternative')
        attachment.preamble = 'This is a multi-part message in MIME format.'
        attachment.attach(MIMEText(plain, _charset='utf-8'))
        attachment.attach(MIMEText(html, 'html', _charset='utf-8'))
    else:
        attachment = MIMEText(content.encode("utf-8"), "plain", "utf-8")
    message.attach(attachment)

def create_attachment(filename, content, mime):
    attachment = MIMEBase(*mime)
    attachment.add_header("Content-Disposition", "attachment", filename=filename)
    attachment.set_payload(content)
    encoders.encode_base64(attachment)
    return attachment

def add_attachment(message, filename, content, mime):
    attachment = create_attachment(filename, content, mime)
    message.attach(attachment)

def create_email(sender, recipients, subject, message_contents, attachments, cc_recipients):
    message = create_message(sender, recipients, cc_recipients, subject)
    attach_message(message, message_contents)
    for filename, content, mime in attachments:
        add_attachment(message, filename, content, mime)
    return message

def send_mail(sender, all_recievers, message, host_server):
    smtp = smtplib.SMTP()
    #smtp.set_debuglevel(True)
    smtp.connect(host_server)

    try:
        smtp.rset()
        smtp.sendmail(sender, all_recievers, message.as_string())
    finally:
        smtp.close()

def get_addresses_from_recipient_list(addresses):
    results = [address if isinstance(address, basestring) else address[1] for address in addresses]
    return [address for address in results if address.strip()]

def find_mail_servers(host_server):
    import dns.resolver
    mx_records = list(dns.resolver.query(host_server, 'MX'))
    mx_records.sort(key=lambda mx: mx.preference)
    return [mx.exchange.to_text() for mx in mx_records]

def img_sendmail(sender, recipients, subject, message_contents, attachments, cc_recipients=[], delay=0, host_server=None, spoof_email_address="codescape@example.com", domain="mips.com"):
    """ Send an email through the IMG SMTP servers.

    sender:             A tuple of the sender name and sender email address.
    recipients:         A sequence of tuple of the recipient name and recipient email address.
    subject:            The message subject header.
    message_contents:   The message body. This can either be a string, in which case it is treated as plain.
                        Or it can be a tuple of (plain text, html).
    attachments:        A sequence of (filename, file contents, mime type).
    cc_recipients:      Carbon copy recipients.

    """

    if host_server is not None:
        mail_servers = [host_server]
    else:
        mail_servers = find_mail_servers(domain)

    message = create_email(sender, recipients, subject, message_contents, attachments, cc_recipients)

    all_receivers = get_addresses_from_recipient_list(recipients) + get_addresses_from_recipient_list(cc_recipients)
    all_receivers = list(set(all_receivers))
    if not all_receivers:
        raise ValueError("No recievers")

    from time import sleep
    sleep(delay)

    for mail_server in mail_servers[:-1]:
        try:
            send_mail(spoof_email_address, all_receivers, message, mail_server)
        except Exception:
            pass
    send_mail(spoof_email_address, all_receivers, message, mail_servers[-1])

def img_sendmail_internal(sender, recipients, subject, message_contents, attachments, cc_recipients=[], delay=0):
    """ Send an email through the internal IMG SMTP servers. Sends an email
    without transporting across the web.

    sender:             A tuple of the sender name and sender email address.
    recipients:         A sequence of tuple of the recipient name and recipient email address.
    subject:            The message subject header.
    message_contents:   The message body. This can either be a string, in which case it is treated as plain.
                        Or it can be a tuple of (plain text, html).
    attachments:        A sequence of (filename, file contents, mime type).
    cc_recipients:      Carbon copy recipients.

    """
    host_server = "mipsmail01.mipstec.com"
    spoof_email_address = "codescape@example.com"
    img_sendmail(sender, recipients, subject, message_contents, attachments, cc_recipients, delay, host_server, spoof_email_address)

if __name__ == '__main__':
    user = os.environ.get('USERNAME') or os.environ.get('LOGNAME')
    who = (user.replace('.', ' ').title(), user + '@mips.com')
    img_sendmail_internal(
        sender = who,
        recipients = [who],
        subject = 'Test Email Message',
        message_contents = 'just a test, delete me',
        attachments = [],
    )
    img_sendmail_internal(
        sender = who,
        recipients = [who],
        subject = 'Test Email Message',
        message_contents = ('just a test, delete me', '<html><body>Just a html test, <b>delete me</b></body></html>'),
        attachments = [],
    )
