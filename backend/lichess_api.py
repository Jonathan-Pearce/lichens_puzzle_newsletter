import requests
import chess
import chess.pgn
import json
from io import StringIO

LICHESS_API_BASE = "https://lichess.org/api"

def fetch_recent_games(username, max_games=10):
    """
    Fetch recent games for a Lichess user.
    
    Args:
        username: Lichess username
        max_games: Maximum number of games to fetch
    
    Returns:
        List of game data dictionaries
    """
    url = f"{LICHESS_API_BASE}/games/user/{username}"
    headers = {
        "Accept": "application/x-ndjson"
    }
    params = {
        "max": max_games,
        "rated": "true",
        "perfType": "blitz,rapid,classical",
        "moves": "true",
        "pgnInJson": "true"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        games = []
        for line in response.text.strip().split('\n'):
            if line:
                game = json.loads(line)
                games.append(game)
        
        return games
    except requests.RequestException as e:
        print(f"Error fetching games for {username}: {e}")
        return []

def analyze_game_for_mistakes(pgn_text, player_color):
    """
    Analyze a game and find instructive mistakes.
    
    Args:
        pgn_text: PGN string of the game
        player_color: 'white' or 'black'
    
    Returns:
        List of mistake positions with context
    """
    pgn = StringIO(pgn_text)
    game = chess.pgn.read_game(pgn)
    
    if not game:
        return []
    
    board = game.board()
    mistakes = []
    move_number = 1
    
    # Iterate through moves
    for node in game.mainline():
        move = node.move
        
        # Simple heuristic: detect potential mistakes
        # In a real implementation, you'd use a chess engine like Stockfish
        # For now, we'll identify moves that lose material or miss captures
        
        legal_moves = list(board.legal_moves)
        
        # Check if there were better captures available
        capture_moves = [m for m in legal_moves if board.is_capture(m)]
        
        # Determine whose turn it is
        is_player_turn = (board.turn == chess.WHITE and player_color == 'white') or \
                        (board.turn == chess.BLACK and player_color == 'black')
        
        if is_player_turn and len(mistakes) < 3:
            # Check for blunders (moves that lose material)
            if board.is_capture(move):
                # Player made a capture, might be good
                pass
            elif capture_moves and not board.is_check():
                # Player missed a capture opportunity
                mistakes.append({
                    'position': board.fen(),
                    'move_number': move_number,
                    'player_move': board.san(move),
                    'hint': 'Look for tactical opportunities',
                    'best_moves': [board.san(m) for m in capture_moves[:3]]
                })
        
        board.push(move)
        if board.turn == chess.WHITE:
            move_number += 1
    
    return mistakes[:3]  # Return top 3 mistakes

def get_puzzles_for_user(lichess_username):
    """
    Get puzzle positions for a user based on their recent games.
    
    Args:
        lichess_username: Lichess username
    
    Returns:
        List of puzzle dictionaries with positions and solutions
    """
    games = fetch_recent_games(lichess_username, max_games=5)
    
    all_mistakes = []
    
    for game_data in games:
        if 'pgn' not in game_data:
            continue
        
        pgn_text = game_data['pgn']
        
        # Determine the user's color in this game
        white_player = game_data.get('players', {}).get('white', {}).get('user', {}).get('name', '').lower()
        player_color = 'white' if white_player == lichess_username.lower() else 'black'
        
        mistakes = analyze_game_for_mistakes(pgn_text, player_color)
        all_mistakes.extend(mistakes)
        
        if len(all_mistakes) >= 3:
            break
    
    # If we don't have 3 mistakes, create some default positions
    while len(all_mistakes) < 3:
        all_mistakes.append({
            'position': chess.STARTING_FEN,
            'move_number': 1,
            'player_move': 'N/A',
            'hint': 'Analyze this position for the best move',
            'best_moves': ['e4', 'd4', 'Nf3']
        })
    
    return all_mistakes[:3]
