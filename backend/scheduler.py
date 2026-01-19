from apscheduler.schedulers.background import BackgroundScheduler
from database import get_all_users, update_newsletter_sent
from lichess_api import get_puzzles_for_user
from pdf_generator import generate_puzzle_pdf
from email_service import send_newsletter_email
import os
import tempfile
from datetime import datetime

def generate_and_send_newsletter(user):
    """
    Generate and send newsletter for a single user.
    
    Args:
        user: User dictionary with id, email, and lichess_username
    """
    print(f"Generating newsletter for {user['email']} ({user['lichess_username']})")
    
    pdf_path = None
    try:
        # Get puzzles from user's games
        puzzles = get_puzzles_for_user(user['lichess_username'])
        
        if not puzzles:
            print(f"No puzzles found for {user['lichess_username']}")
            return
        
        # Generate PDF with a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.pdf', delete=False) as tmp_file:
            pdf_path = tmp_file.name
        
        generate_puzzle_pdf(puzzles, pdf_path)
        
        # Send email
        success = send_newsletter_email(user['email'], pdf_path, user['lichess_username'])
        
        if success:
            update_newsletter_sent(user['id'])
            print(f"Newsletter sent successfully to {user['email']}")
            
    except Exception as e:
        print(f"Error generating newsletter for {user['email']}: {e}")
    finally:
        # Clean up PDF in finally block to ensure cleanup happens
        if pdf_path and os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
            except Exception as e:
                print(f"Error removing temporary file {pdf_path}: {e}")

def send_newsletters_to_all_users():
    """Send newsletters to all registered users."""
    print(f"Starting newsletter generation at {datetime.now()}")
    users = get_all_users()
    
    for user in users:
        generate_and_send_newsletter(user)
    
    print(f"Newsletter generation completed at {datetime.now()}")

def start_scheduler():
    """Start the background scheduler for weekly newsletters."""
    scheduler = BackgroundScheduler()
    
    # Schedule for every Monday at 9:00 AM
    scheduler.add_job(
        send_newsletters_to_all_users,
        'cron',
        day_of_week='mon',
        hour=9,
        minute=0
    )
    
    scheduler.start()
    print("Newsletter scheduler started - will run every Monday at 9:00 AM")
    return scheduler
