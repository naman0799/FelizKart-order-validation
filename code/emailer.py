from email.message import EmailMessage
import ssl
import smtplib
import os


def sendmail(subject, body, recipient_email='abc123@gmail.com', simulate=True):
    """ Sends an email with the given subject and body. """
    email_sender = 'xyz789@gmail.com'
    email_password = os.getenv('EMAIL_APP_PASSWORD')
    if simulate:
        print("[Simulated Email]")
        print(f"To: {recipient_email}")
        print(f"Subject: {subject}")
        print("Body:\n", body)
        return

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = recipient_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(em)
        print("Email sent successfully.")

    except Exception as e:
        print("Failed to send email:", e)
