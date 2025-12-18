import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.config import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

def send_email(receiver_email: str, otp: int) -> bool:
    SMTP_HOST = EMAIL_HOST
    SMTP_PORT = EMAIL_PORT
    SMTP_USER = EMAIL_HOST_USER
    SMTP_PASS = EMAIL_HOST_PASSWORD

    try:
        # Create message container
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "{otp}-Verification Code - Product Studio"
        msg["From"] = SMTP_USER
        msg["To"] = receiver_email

        # HTML Email Body
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset='UTF-8'>
            <meta name='viewport' content='width=device-width, initial-scale=1.0'>
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background-color: #f8f9fa;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    max-width: 600px;
                    margin: auto;
                    background: #ffffff;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .title {{
                    color: #1a237e;
                    font-size: 24px;
                    font-weight: 600;
                    margin: 0;
                }}
                .otp-container {{
                    background: #f5f7ff;
                    border: 1px solid #e3e9ff;
                    border-radius: 8px;
                    padding: 20px;
                    margin: 25px 0;
                    text-align: center;
                }}
                .otp-code {{
                    font-family: 'Courier New', monospace;
                    font-size: 32px;
                    font-weight: bold;
                    color: #1a237e;
                    letter-spacing: 4px;
                    margin: 10px 0;
                }}
                .warning {{
                    background: #fff8e1;
                    border-left: 4px solid #ffa000;
                    padding: 15px;
                    margin: 20px 0;
                    font-size: 14px;
                    color: #666;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    font-size: 12px;
                    color: #757575;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class='email-container'>
                <div class='header'>
                    <h1 class='title'>Secure Verification Required</h1>
                </div>
                
                <p style='color:#424242; font-size:16px'>
                    Thank you for choosing Product Studio. Use the verification code below to continue.
                </p>
                
                <div class='otp-container'>
                    <p style='margin: 0; color: #666;'>Your verification code is:</p>
                    <div class='otp-code'>{otp}</div>
                    <p style='margin: 5px 0; color: #666;'>This code will expire in 10 minutes</p>
                </div>

                <div class='warning'>
                    <strong>Security Notice:</strong> If you didn't request this verification code, contact support immediately at support@productstudio.in
                </div>

                <div class='footer'>
                    <p>This is an automated message, do not reply.</p>
                    <p>© 2025 Product Studio. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, "html"))

        # Send email securely over SSL
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, receiver_email, msg.as_string())

        return True

    except Exception as e:
        print("Email sending failed:", e)
        return False


