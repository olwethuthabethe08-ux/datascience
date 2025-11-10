import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password_here"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(recipient, subject, body, attachments=None):
    """Send an email with optional attachments."""
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "html"))

        # Add attachments
        if attachments:
            for file_path in attachments:
                with open(file_path, "rb") as f:
                    file_name = os.path.basename(file_path)
                    part = MIMEApplication(f.read(), Name=file_name)
                    part['Content-Disposition'] = f'attachment; filename="{file_name}"'
                    msg.attach(part)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f"Email sent successfully to {recipient}")
        return True
    except Exception as e:
        print(f" Failed to send email to {recipient}: {e}")
        return False


# ------------------- EMAIL FEATURES -------------------

def send_welcome_email(student_email, student_name):
    """Send a welcome email to a new student."""
    subject = " Welcome to Our Course Platform!"
    body = f"""
    <html>
        <body>
            <h2>Welcome, {student_name}!</h2>
            <p>We're excited to have you join our learning community.</p>
            <p>You can now log in, enroll in courses, and begin your learning journey.</p>
            <br>
            <p>Best regards,<br>The Course Management Team</p>
        </body>
    </html>
    """
    return send_email(student_email, subject, body)


def send_grade_report(student_email, student_name, grade_details):
    """Send grade report email."""
    subject = "Your Grade Report"
    body = f"""
    <html>
        <body>
            <h2>Hello {student_name},</h2>
            <p>Here are your latest grades:</p>
            <p>{grade_details}</p>
            <br>
            <p>Keep up the great work!</p>
        </body>
    </html>
    """
    return send_email(student_email, subject, body)


def send_bulk_announcement(student_emails, announcement_title, message):
    """Send one announcement to many students."""
    subject = f" {announcement_title}"
    body = f"""
    <html>
        <body>
            <h2>{announcement_title}</h2>
            <p>{message}</p>
            <br>
            <p>— Course Management System</p>
        </body>
    </html>
    """
    for email in student_emails:
        send_email(email, subject, body)


def send_transcript_or_certificate(student_email, student_name, file_path):
    """Email a transcript or certificate file."""
    subject = f" Transcript/Certificate for {student_name}"
    body = f"""
    <html>
        <body>
            <h2>Dear {student_name},</h2>
            <p>Please find attached your transcript/certificate.</p>
            <br>
            <p>Congratulations on your hard work!</p>
        </body>
    </html>
    """
    return send_email(student_email, subject, body, attachments=[file_path])



