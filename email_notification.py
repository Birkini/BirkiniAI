import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_mail import Mail, Message
from flask import Flask, render_template

# Flask application setup
app = Flask(__name__)

# Flask-Mail setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'your_email_password'  # Your email password
mail = Mail(app)

def send_email(subject, recipient, body):
    """Send email notifications to users."""
    try:
        msg = MIMEMultipart()
        msg['From'] = app.config['MAIL_USERNAME']
        msg['To'] = recipient
        msg['Subject'] = subject
        
        # Attach the body of the email to the MIME message
        msg.attach(MIMEText(body, 'plain'))
        
        # Set up the server and send the email
        server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        server.starttls()
        server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        
        print(f"Email sent successfully to {recipient}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

@app.route('/send_notification/<user_email>')
def send_notification(user_email):
    """Send a notification email to a user."""
    subject = "Your Data Processing is Complete"
    body = "Hello, your data has been successfully processed. You can now view the results in your dashboard."
    
    send_email(subject, user_email, body)
    return f"Notification sent to {user_email}"

if __name__ == "__main__":
    app.run(debug=True)
