from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from database import init_db, add_user, get_all_users
from scheduler import start_scheduler, generate_and_send_newsletter
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Allow requests from GitHub Pages and localhost
allowed_origins = [
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "https://jonathan-pearce.github.io"
]
CORS(app, origins=allowed_origins)

# Initialize database
init_db()

# Start scheduler for weekly newsletters
scheduler = start_scheduler()

@app.route('/')
def serve_frontend():
    """Serve the frontend HTML file."""
    return send_from_directory('../frontend', 'index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'Chess Puzzle Newsletter API is running'})

@app.route('/api/signup', methods=['POST'])
def signup():
    """
    User signup endpoint.
    
    Expected JSON body:
    {
        "email": "user@example.com",
        "lichess_username": "username"
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email = data.get('email', '').strip()
    lichess_username = data.get('lichess_username', '').strip()
    
    # Validation
    if not email or '@' not in email:
        return jsonify({'error': 'Valid email is required'}), 400
    
    if not lichess_username:
        return jsonify({'error': 'Lichess username is required'}), 400
    
    # Add user to database
    success, message = add_user(email, lichess_username)
    
    if success:
        return jsonify({'success': True, 'message': message}), 201
    else:
        return jsonify({'success': False, 'error': message}), 409

@app.route('/api/users', methods=['GET'])
def list_users():
    """List all registered users (for admin purposes)."""
    users = get_all_users()
    return jsonify({'users': users, 'count': len(users)})

@app.route('/api/test-newsletter/<int:user_id>', methods=['POST'])
def test_newsletter(user_id):
    """
    Test endpoint to generate and send newsletter for a specific user.
    Useful for testing without waiting for the weekly schedule.
    """
    users = get_all_users()
    user = next((u for u in users if u['id'] == user_id), None)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        generate_and_send_newsletter(user)
        return jsonify({'success': True, 'message': f'Newsletter sent to {user["email"]}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
