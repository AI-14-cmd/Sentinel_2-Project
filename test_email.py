import smtplib
from email.mime.text import MIMEText

EMAIL_SENDER = "aniruddhneje@gmail.com"  # Your Gmail address
EMAIL_PASSWORD = "qqfl vyzl bfpd plsz"  # Your 16-character Gmail App Password
EMAIL_RECIPIENT = "nejeaniruddh@gmail.com"  # Where you want to receive the test email

msg = MIMEText("This is a test email from your Python script.")
msg["Subject"] = "SMTP Test Email"
msg["From"] = EMAIL_SENDER
msg["To"] = EMAIL_RECIPIENT

try:
    print("Connecting to Gmail SMTP server...")
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    print("Sending test email...")
    server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())
    server.quit()
    print("Test email sent successfully!")
except Exception as e:
    print(f"Error sending test email: {e}") 