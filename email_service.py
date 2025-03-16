import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")

    def send_report(self, recipient_email, stock_symbol, analysis_data):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = recipient_email
            msg['Subject'] = f"Stock Analysis Report - {stock_symbol}"

            # Create email body
            body = f"Analysis Report for {stock_symbol}\n\n"
            for quarter_data in analysis_data:
                body += f"Quarter: {quarter_data['Quarter']}\n"
                body += f"Interest Income: ${quarter_data['Interest Income']:,.2f}\n"
                body += f"Interest per Share: ${quarter_data['Interest per Share']:,.2f}\n"
                body += f"Interest/Net Income Ratio: {quarter_data['Interest/Net Income Ratio']:.2f}%\n\n"

            msg.attach(MIMEText(body, 'plain'))

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")
