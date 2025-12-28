import json
import pygame
import os
from .util_params import *

def load_high_scores():
    """Lengths the high scores from the JSON file. Returns empty list if file not found or error."""
    if not os.path.exists(HIGH_SCORE_FILE):
        return []
    
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            scores = json.load(f)
            return scores
    except Exception as e:
        print(f"Error loading scores: {e}")
        return []

def get_score_from_entry(entry):
    return entry['score']

def save_high_scores(scores, player_name, new_score):
    """Updates the high scores list with the new score, keeps top 5, and saves to file."""
    player_found = False
    
    # Check if player already exists in the list
    for entry in scores:
        if entry['name'] == player_name:
            player_found = True
            if new_score > entry['score']:
                entry['score'] = new_score
            break
            
    # If new player, add them
    if not player_found:    
        new_entry = {'name': player_name, 'score': new_score}
        scores.append(new_entry)
        
    # Sort scores descending
    sorted_scores = sorted(scores, key=get_score_from_entry, reverse=True)
    
    # Keep only top 5
    top_5_scores = sorted_scores[:5]
    
    try:
        with open(HIGH_SCORE_FILE, 'w') as f:
            json.dump(top_5_scores, f, indent=4)
    except Exception as e:
        print(f"Error saving scores: {e}")
        
    return top_5_scores


