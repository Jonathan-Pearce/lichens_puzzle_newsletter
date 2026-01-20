import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

def send_newsletter_email(to_email, pdf_path, lichess_username):
    """
    Send the puzzle newsletter email with PDF attachment.
    
    Args:
        to_email: Recipient email address
        pdf_path: Path to the PDF file
        lichess_username: User's Lichess username
    
    Returns:
        True if successful, False otherwise
    """
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL', smtp_username)
    
    if not smtp_username or not smtp_password:
        print("SMTP credentials not configured")
        return False
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = f"Your Weekly Chess Puzzles - {lichess_username}"
    
    # Email body
    body = f"""
    Hello {lichess_username}!
    
    Here's your personalized weekly chess puzzle newsletter based on your recent games on Lichess.
    
    We've analyzed your games and selected 3 instructive positions where you can improve your play.
    
    The attached PDF contains:
    - Page 1: Three puzzle positions for you to solve
    - Page 2: Solutions with best moves and explanations
    
    Keep practicing and improving your chess skills!
    
    Best regards,
    The Chess Puzzle Newsletter Team
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach PDF
    try:
        with open(pdf_path, 'rb') as f:
            pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
            pdf_attachment.add_header('Content-Disposition', 'attachment', 
                                     filename=f'chess_puzzles_{lichess_username}.pdf')
            msg.attach(pdf_attachment)
    except FileNotFoundError:
        print(f"PDF file not found: {pdf_path}")
        return False
    
    # Send email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        print(f"Newsletter sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")
        return False
