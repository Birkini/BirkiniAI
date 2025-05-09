import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask application setup
app = Flask(__name__)

# Load mail configuration from environment variables
app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
    MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS', 'true').lower() in ('true', '1', 'yes'),
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER', os.getenv('MAIL_USERNAME')),
)

mail = Mail(app)

def send_email(subject: str, recipient: str, template_name: str, **context) -> None:
    """
    Send an email using Flask-Mail with both text and HTML templates.

    :param subject: Email subject
    :param recipient: Recipient email address
    :param template_name: Base name of the templates (without extension)
    :param context: Variables to pass into the templates
    """
    msg = Message(subject=subject, recipients=[recipient])
    msg.body = render_template(f'{template_name}.txt', **context)
    msg.html = render_template(f'{template_name}.html', **context)

    try:
        mail.send(msg)
        logger.info(f"Email sent to {recipient}: {subject}")
    except Exception as e:
        logger.exception(f"Failed to send email to {recipient}")

@app.route('/send_notification', methods=['POST'])
def send_notification():
    """
    Send a notification email.
    Expects JSON payload:
    {
      "email": "<recipient_email>",
      "subject": "<email_subject>",
      "message": "<plain_text_message>"
    }
    """
    data = request.get_json() or {}
    email = data.get('email')
    subject = data.get('subject', 'Notification from Birkini')
    message = data.get('message', '')

    if not email:
        return jsonify({"error": "Missing 'email' field"}), 400

    send_email(subject, email, 'notification', message=message)
    return jsonify({"message": f"Notification sent to {email}"}), 200

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() in ('true', '1', 'yes')
    app.run(debug=debug_mode)
