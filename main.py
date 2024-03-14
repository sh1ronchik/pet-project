import imaplib
import email
from bs4 import BeautifulSoup
from email.utils import parsedate_to_datetime, parseaddr

def get_latest_email():
    mail = imaplib.IMAP4_SSL('imap.yandex.ru')
    mail.login('email', 'spec_pass')
    mail.select("inbox")
    result, data = mail.search(None, "ALL")
    latest_email_id = data[0].split()[-1]
    result, data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email_string = data[0][1].decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    return email_message

def print_email_details(email_message):
    to = parseaddr(email_message['To'])[1]
    from_ = parseaddr(email_message['From'])[1]
    date = parsedate_to_datetime(email_message['Date']).strftime('%Y-%m-%d %H:%M:%S')
    print(f'To: {to}')
    print(f'From: {from_}')
    print(f'Date: {date}')

def print_email_body(email_message):
    print('Text:')
    if email_message.is_multipart():
        for payload in email_message.get_payload():
            body = payload.get_payload(decode=True).decode('utf-8')
            soup = BeautifulSoup(body, 'html.parser')
            text = soup.get_text()
            print(text)
    else:
        body = email_message.get_payload(decode=True).decode('utf-8')
        soup = BeautifulSoup(body, 'html.parser')
        text = soup.get_text()
        print(text)

email_message = get_latest_email()
print_email_details(email_message)
print_email_body(email_message)