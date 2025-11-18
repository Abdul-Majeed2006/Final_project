import json
import pygame
from util_params import *
#name of file
Filename = 'high_scores.json'

def load_high_scores():
    try:# we dont have the json file yet
        with open(Filename,'r') as f:
            scores = json.load(f)
            return scores
    except Exception as e:
        return[]
def get_score_from_entry(entry):
    return entry['score']
def save_high_scores(scores,player_name,new_score):
    player_found = False
    for entry in scores:
        if entry['name'] == player_name:
            player_found = True
            if new_score > entry['score']:
                entry['score'] = new_score
            #player found break the rest of the loop
            break
    #update if thier name is not in top 5
    if not player_found:    
        #create new entry
        new_entry = {'name': player_name,'score':new_score}
        #add the new entry to the list
        scores.append(new_entry)
    #lets sort the scores
    sorted_scores = sorted(scores,key=get_score_from_entry,reverse=True)
    #keep only top 5 scores
    top_5_scores = sorted_scores[:5]
    with open(Filename,'w') as f:
        json.dump(top_5_scores,f,indent=4)
    return top_5_scores
# draw the scores function
def draw_high_scores(surface,scores):
    score_title_font = pygame.font.SysFont('Arial',30)
    score_font = pygame.font.SysFont('Arial',24)
    title_text = score_title_font.render('High Scores',True,(255,255,0))
    title_rect = title_text.get_rect(center=(WIDTH/2,50))
    surface.blit(title_text,title_rect)
    y = 100
    for i, entry in enumerate(scores):
        entry_text = f'{i+1}. {entry['name']} - {entry['score']}'
        score_text = score_font.render(entry_text,True,(255,255,255))
        score_rect = score_text.get_rect(center=(WIDTH/2,y))
        surface.blit(score_text,score_rect)
        y+=28