import os
import smtplib
import config

class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.

    def __init__(self):
        self.smtp = os.environ.get("GMAIL_SMTP")
        self.smtp_port = int(os.environ.get("GMAIL_SMTP_PORT"))
        self.test_sender_email = os.environ.get("GMAIL_TEST_EMAIL")
        self.sender_app_pwd = os.environ.get("GMAIL_TEST_APP_PWD")

    def send_emails(self, emails_list, msg_body):
        try:
            with smtplib.SMTP(self.smtp, self.smtp_port) as connection:
                connection.starttls()
                connection.login(self.test_sender_email, self.sender_app_pwd)
                for email in emails_list:
                    connection.sendmail(self.test_sender_email, email, msg_body)
            print("Message sent")
        except smtplib.SMTPAuthenticationError:
            print("Error: Authentication failed. Check email and password.")
        except smtplib.SMTPConnectError:
            print("Error: Unable to connect to the SMTP server.")
        except smtplib.SMTPRecipientsRefused:
            print("Error: All recipient addresses were rejected.")
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
