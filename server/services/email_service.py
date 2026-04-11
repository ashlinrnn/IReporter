import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from sib_api_v3_sdk import SendSmtpEmail, SendSmtpEmailTo, SendSmtpEmailSender

def send_status_update_email(recipient_email, recipient_name, record_title, new_status):
    """
    Sends a transactional email using Brevo's API (official sib-api-v3-sdk).
    """
    # Configure API key authorization
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')
    
    # Create an instance of the API class
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # Prepare email content
    subject = f"Update on your iReporter report: '{record_title}'"
    sender = SendSmtpEmailSender(
        name="iReporter Team",
        email=os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@ireporter.com')
    )
    to_emails = [SendSmtpEmailTo(email=recipient_email, name=recipient_name)]
    
    html_content = f"""
    <html>
        <body>
            <p>Hello {recipient_name},</p>
            <p>The status of your report <strong>'{record_title}'</strong> has been updated to: <strong>{new_status}</strong>.</p>
            <p>Thank you for using iReporter.</p>
        </body>
    </html>
    """

    send_smtp_email = SendSmtpEmail(
        to=to_emails,
        sender=sender,
        subject=subject,
        html_content=html_content
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Email sent to {recipient_email}. Message ID: {api_response.message_id}")
        return True
    except ApiException as e:
        print(f"Exception when sending email: {e}")
        return False

def send_password_reset_email(recipient_email, recipient_name, reset_link):
    """
    Sends a password reset email with a link.
    """
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    subject = "Reset your iReporter password"
    sender = {"name": "iReporter Team", "email": os.environ.get('MAIL_DEFAULT_SENDER')}
    to_emails = [{"email": recipient_email, "name": recipient_name}]
    
    html_content = f"""
    <html>
        <body>
            <p>Hello {recipient_name},</p>
            <p>We received a request to reset your iReporter account password.</p>
            <p>Click the link below to set a new password (valid for 1 hour):</p>
            <p><a href="{reset_link}">Reset Password</a></p>
            <p>If you didn't request this, please ignore this email.</p>
            <p>Thank you,<br>iReporter Team</p>
        </body>
    </html>
    """
    
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to_emails,
        sender=sender,
        subject=subject,
        html_content=html_content
    )
    try:
        api_instance.send_transac_email(send_smtp_email)
        print(f"Password reset email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send reset email: {e}")