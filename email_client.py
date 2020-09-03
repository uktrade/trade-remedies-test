import imaplib
import email
from time import sleep
from collections import namedtuple
from datetime import datetime, timedelta

from configuration import EMAIL_ACCOUNT, EMAIL_PASSWORD

Email = namedtuple('Email', ['date', 'sender', 'subject', 'body'])


def check_for_email(with_subject, addressed_to, later_than, timeout=10*60, account=EMAIL_ACCOUNT, password=EMAIL_PASSWORD):
    assert password is not None
    emails = []
    start_time = datetime.now()
    while datetime.now() <= start_time + timedelta(seconds=timeout):
        emails = get_emails(addressed_to=addressed_to, later_than=later_than, account=account, password=password)
        for email_ in emails:
            if with_subject == email_.subject:
                return email_
        sleep(2)  # Don't spam the IMAP server
    else:
        error_message = "Timed out waiting for an email with subject {} addressed to {} later than {}".format(
            with_subject,
            addressed_to,
            later_than
        )
        if emails:
            error_message += ". Saw emails with subject lines {}.".format([e.subject for e in emails])
        raise TimeoutError(error_message)


def get_emails(addressed_to, with_subject=None, later_than=None, account=EMAIL_ACCOUNT, password=EMAIL_PASSWORD, delay=0):

    sleep(delay)

    emails = []

    mail = imaplib.IMAP4_SSL('imap-mail.outlook.com', 993)
    mail.login(account, password)
    mail.select('inbox')

    _, data = mail.search(None, 'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()
    if not id_list:
        return emails
    first_email_id = int(id_list[0])
    last_email_id = int(id_list[-1])

    for index in range(last_email_id, first_email_id-1, -1):
        _, data = mail.fetch(str(index), '(RFC822)')
        response_part = data[0]
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            email_subject = _decode_header(msg['subject']).replace('\r\n', '').replace('\xa0', ' ').replace('’', "'")
            email_from = msg['from']
            # TODO: Fix this decoding
            email_body = msg.get_payload(1).as_bytes().decode('utf-8').replace('=\n', '').replace('=E2=80=93', '-').replace('=E2=80=99', "'")
            email_date = datetime.strptime(msg['date'], '%a, %d %b %Y %H:%M:%S %z')
            if later_than is not None and email_date < later_than:
                break
            if with_subject is not None and with_subject != email_subject:
                continue
            if addressed_to in email_body:
                emails.append(Email(date=email_date, sender=email_from, subject=email_subject, body=email_body))

    mail.logout()

    return emails


def _decode_header(encoded_header):
    decoded = email.header.decode_header(encoded_header)[0][0]
    if isinstance(decoded, str):
        return decoded
    elif isinstance(decoded, bytes):
        decoded = decoded.decode('utf-8')
        return decoded
    else:
        raise TypeError

