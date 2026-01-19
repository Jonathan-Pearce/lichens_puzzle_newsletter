from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, white, HexColor
import chess
import chess.svg
from io import BytesIO
import os

def draw_chessboard(c, x, y, size, board_fen):
    """
    Draw a chess board on the PDF canvas.
    
    Args:
        c: ReportLab canvas
        x, y: Position coordinates
        size: Size of the board in points
        board_fen: FEN string representing the position
    """
    board = chess.Board(board_fen)
    square_size = size / 8
    
    # Draw squares
    for rank in range(8):
        for file in range(8):
            is_light = (rank + file) % 2 == 0
            color = HexColor('#F0D9B5') if is_light else HexColor('#B58863')
            
            square_x = x + file * square_size
            square_y = y + (7 - rank) * square_size
            
            c.setFillColor(color)
            c.rect(square_x, square_y, square_size, square_size, fill=1, stroke=0)
    
    # Draw pieces using Unicode chess symbols
    piece_symbols = {
        'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
        'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
    }
    
    c.setFillColor(black)
    for rank in range(8):
        for file in range(8):
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            
            if piece:
                piece_char = piece.symbol()
                symbol = piece_symbols.get(piece_char, '')
                
                square_x = x + file * square_size
                square_y = y + (7 - rank) * square_size
                
                # Set color for piece
                if piece.color == chess.WHITE:
                    c.setFillColor(HexColor('#FFFFFF'))
                    c.setStrokeColor(black)
                else:
                    c.setFillColor(black)
                
                # Draw piece symbol
                c.setFont("Helvetica", int(square_size * 0.8))
                c.drawString(square_x + square_size * 0.15, square_y + square_size * 0.1, symbol)

def generate_puzzle_pdf(puzzles, output_path):
    """
    Generate a 2-page PDF with chess puzzles.
    
    Page 1: Questions (3 board positions)
    Page 2: Answers (evaluations and best moves)
    
    Args:
        puzzles: List of puzzle dictionaries
        output_path: Path to save the PDF
    """
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Page 1: Questions
    c.setFont("Helvetica-Bold", 24)
    c.drawString(inch, height - inch, "Your Weekly Chess Puzzles")
    
    c.setFont("Helvetica", 12)
    c.drawString(inch, height - inch - 0.3 * inch, "Find the best move in each position")
    
    board_size = 2 * inch
    y_positions = [height - 2.5 * inch, height - 5 * inch, height - 7.5 * inch]
    
    for idx, puzzle in enumerate(puzzles[:3]):
        y_pos = y_positions[idx]
        
        # Draw puzzle number and hint
        c.setFont("Helvetica-Bold", 14)
        c.drawString(inch, y_pos + board_size + 0.2 * inch, f"Puzzle {idx + 1}")
        
        c.setFont("Helvetica", 10)
        c.drawString(inch, y_pos + board_size, f"Move {puzzle['move_number']} - White to move" if 'white' in puzzle.get('position', '') else f"Move {puzzle['move_number']}")
        
        # Draw chess board
        draw_chessboard(c, inch, y_pos, board_size, puzzle['position'])
        
        # Draw hint
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(inch + board_size + 0.5 * inch, y_pos + board_size / 2, f"Hint: {puzzle['hint']}")
    
    # Page 2: Answers
    c.showPage()
    
    c.setFont("Helvetica-Bold", 24)
    c.drawString(inch, height - inch, "Solutions")
    
    y_pos = height - 1.8 * inch
    
    for idx, puzzle in enumerate(puzzles[:3]):
        c.setFont("Helvetica-Bold", 14)
        c.drawString(inch, y_pos, f"Puzzle {idx + 1} - Solution")
        y_pos -= 0.3 * inch
        
        c.setFont("Helvetica", 11)
        c.drawString(inch + 0.2 * inch, y_pos, f"Position: Move {puzzle['move_number']}")
        y_pos -= 0.25 * inch
        
        c.drawString(inch + 0.2 * inch, y_pos, f"Your move was: {puzzle.get('player_move', 'N/A')}")
        y_pos -= 0.25 * inch
        
        c.setFont("Helvetica-Bold", 11)
        c.drawString(inch + 0.2 * inch, y_pos, "Best moves:")
        y_pos -= 0.25 * inch
        
        c.setFont("Helvetica", 10)
        for move in puzzle.get('best_moves', [])[:3]:
            c.drawString(inch + 0.4 * inch, y_pos, f"• {move}")
            y_pos -= 0.2 * inch
        
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(inch + 0.2 * inch, y_pos, f"Key idea: {puzzle['hint']}")
        y_pos -= 0.5 * inch
    
    c.setFont("Helvetica", 10)
    c.drawString(inch, inch, "Keep practicing! Visit lichess.org for more puzzles.")
    
    c.save()
    return output_path
