# Chess Puzzle Newsletter

A personalized chess puzzle newsletter system that analyzes your Lichess games and sends weekly instructive puzzles based on your mistakes.

## Features

- 🎯 **Personalized Puzzles**: Analyzes your recent Lichess games to find instructive positions
- 📧 **Weekly Emails**: Automatically sends PDF newsletters every Monday
- 📊 **2-Page Format**: Questions on page 1, solutions with explanations on page 2
- 🎨 **Beautiful UI**: Clean, modern signup interface
- ♟️ **Chess Board Visualization**: PDFs include visual chess board representations

## Project Structure

```
lichens_puzzle_newsletter/
├── backend/               # Python Flask backend
│   ├── app.py            # Main Flask application
│   ├── database.py       # SQLite database operations
│   ├── lichess_api.py    # Lichess API integration
│   ├── pdf_generator.py  # PDF generation logic
│   ├── email_service.py  # Email sending functionality
│   ├── scheduler.py      # Weekly newsletter scheduler
│   ├── requirements.txt  # Python dependencies
│   └── .env.example      # Environment variables template
└── frontend/             # Frontend UI
    └── index.html        # Signup form (vanilla HTML/JS)
```

## Setup Instructions

### Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   - Copy `.env.example` to `.env`
   - Update the following variables:
     ```
     SMTP_SERVER=smtp.gmail.com
     SMTP_PORT=587
     SMTP_USERNAME=your-email@gmail.com
     SMTP_PASSWORD=your-app-password
     FROM_EMAIL=your-email@gmail.com
     ```
   - For Gmail, you'll need to create an [App Password](https://support.google.com/accounts/answer/185833)

5. **Run the backend**:
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`

### Frontend Setup

1. **Open the frontend**:
   - Simply open `frontend/index.html` in your web browser
   - Or serve it with a simple HTTP server:
     ```bash
     cd frontend
     python -m http.server 8000
     ```
   - Access at `http://localhost:8000`

## Usage

### User Signup

1. Open the frontend in your browser
2. Enter your email address
3. Enter your Lichess username
4. Click "Subscribe to Newsletter"

### Testing the Newsletter

You can test the newsletter generation without waiting for the weekly schedule:

```bash
# Get list of users
curl http://localhost:5000/api/users

# Send test newsletter to a specific user (replace 1 with actual user ID)
curl -X POST http://localhost:5000/api/test-newsletter/1
```

### API Endpoints

- `GET /api/health` - Health check
- `POST /api/signup` - User signup
  ```json
  {
    "email": "user@example.com",
    "lichess_username": "username"
  }
  ```
- `GET /api/users` - List all users
- `POST /api/test-newsletter/<user_id>` - Test newsletter generation

## How It Works

1. **User Signup**: Users register with their email and Lichess username
2. **Game Analysis**: System fetches recent games from Lichess API
3. **Mistake Detection**: Analyzes games to find positions where the user could improve
4. **PDF Generation**: Creates a 2-page PDF with puzzles and solutions
5. **Email Delivery**: Sends the PDF via email every Monday at 9 AM
6. **Continuous Learning**: New puzzles generated from latest games each week

## Technologies Used

### Backend
- **Flask**: Web framework
- **python-chess**: Chess game analysis
- **ReportLab**: PDF generation
- **APScheduler**: Weekly scheduling
- **SQLite**: User database
- **Requests**: Lichess API communication

### Frontend
- **HTML/CSS/JavaScript**: Vanilla web technologies for simplicity
- **Responsive Design**: Works on all devices

## Configuration

### Email Settings

The system uses SMTP for email delivery. Configure in `.env`:

- **Gmail**: Use app-specific passwords
- **Other providers**: Adjust SMTP_SERVER and SMTP_PORT accordingly

### Scheduler

By default, newsletters are sent every Monday at 9:00 AM. To change this, edit `scheduler.py`:

```python
scheduler.add_job(
    send_newsletters_to_all_users,
    'cron',
    day_of_week='mon',  # Change day: mon, tue, wed, thu, fri, sat, sun
    hour=9,              # Change hour (0-23)
    minute=0
)
```

## Development

### Running in Development Mode

Backend runs with Flask debug mode enabled by default. For production:

```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
python app.py
```

### Database

User data is stored in SQLite (`users.db`). The database is automatically created on first run.

## Troubleshooting

**Issue**: Email not sending
- Check SMTP credentials in `.env`
- For Gmail, ensure "Less secure app access" is enabled or use App Passwords
- Check firewall/network settings

**Issue**: No puzzles generated
- Verify Lichess username is correct
- Ensure user has played recent games on Lichess
- Check Lichess API is accessible

**Issue**: Frontend can't connect to backend
- Ensure backend is running on port 5000
- Check CORS settings in `app.py`
- Verify API_URL in `frontend/index.html`

## License

ISC

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.