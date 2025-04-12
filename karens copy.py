import pygame
import random
import time
from google import genai
client = genai.Client(api_key ='URAPI')

import json

def fun(txt):
  response = client.models.generate_content(
      model="gemini-2.0-flash",
      contents=["generate 5 quiz questions based on this text and return questions and 4 multiple choice as a json file with questions named question and options named options and the answer named answer", txt],
  )
  text = response.text
  text = text[len("```json"):]
  text = text[:text.index("```")]
  data= json.loads(text)
  for i in data:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=["can you return a sentence directly from this text that contains the answer to" + i['question'],txt]
        )
    i["highlight"] = response.text
  return data

text = "One of the first organisms that humans domesticated was yeast. In 2011, while excavating an old graveyard in an Armenian cave, scientists discovered a 6,000 year-old winery, complete with a wine press, fermentation vessels, and even drinking cups. This winery was a major technological innovation that required understanding how to control Sacharomyces, the genus of yeast used in alcohol and bread production."


# Initialize Pygame
pygame.init()
pygame.mixer.init()

#define text
user_text = ""
texts = ""
box_color_active = pygame.Color('lightskyblue3')
box_color_inactive = pygame.Color('gray15')
box_color = box_color_inactive

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (129, 167, 144)
DARK_GREEN = (36,130,72)
RED = (255, 0, 0)

# DISPLAY SET UP
window_size = (1100, 700)
display = pygame.display.set_mode(window_size)

# Load and scale background image for the first page
bg_image = pygame.image.load('placeholder_sprites/bc25bk.png')
bg_image = pygame.transform.scale(bg_image, window_size)

# Load and scale background image for the second page
select_fighter_image = pygame.image.load('placeholder_sprites/bc25selectfighter.png')
select_fighter_image = pygame.transform.scale(select_fighter_image, window_size)

# load & scale battle begins
battle_begins_bg_image = pygame.image.load('placeholder_sprites/bc25battlebegins.png')
battle_begins_bg_image = pygame.transform.scale(battle_begins_bg_image, window_size)

# load & scale background image for questions page
question_bg_image = pygame.image.load('placeholder_sprites/bc25question.png')
question_bg_image = pygame.transform.scale(question_bg_image, window_size)

#load & scale background for the ending page
ending_bg_image = pygame.image.load('placeholder_sprites/bc25ending.png')
ending_bg_image = pygame.transform.scale(ending_bg_image, window_size)

intro_text_image = pygame.image.load('placeholder_sprites/bc25howtoplay.png')
intro_text_image = pygame.transform.scale(intro_text_image, (500, 500))

they_attack_image = pygame.image.load('placeholder_sprites/bc25themfireball.png')
they_attack_image = pygame.transform.scale(they_attack_image, window_size)

you_attack_image = pygame.image.load('placeholder_sprites/bc25youfireball.png')
you_attack_image = pygame.transform.scale(you_attack_image, window_size)

# Button properties
button_color = GREEN
button_hover_color = (36, 130, 72)

# Define page states
#score = 0
PAGE_MAIN = 0
INFO_PAGE = 1
PAGE_FIGHTER = 2
PAGE_BATTLE_BEGINS = 3
PAGE_QUESTION = 4
PAGE_ANS = 5
PAGE_YOU_ATTACK = 6
PAGE_THEY_ATTACK = 7
PAGE_TEXT_HIGHLIGHT = 8
PAGE_REDEMPTION = 9
PAGE_ENDING = 10
UPLOAD_PAGE = 11

current_page = PAGE_MAIN

upload_text_button_rect = pygame.Rect(450, 400, 200, 50)
info_button_rect = pygame.Rect(450, 475, 200, 50)

begin_button_rect = pygame.Rect(450, 575, 200, 50)

next1_button_rect = pygame.Rect(450, 650, 200, 50)
next2_button_rect = pygame.Rect(450, 500, 200, 50)
next3_button_rect = pygame.Rect(450, 525, 200, 50)
next4_button_rect = pygame.Rect(450, 575, 200, 50)
next5_button_rect = pygame.Rect(450, 600, 200, 50)
next6_button_rect = pygame.Rect(450, 450, 200, 50)
uploadbox = pygame.Rect(400, 400, 300, 200)
close_button_rect = pygame.Rect(450, 625, 200, 50)

play_again_button_rect = pygame.Rect(450, 500, 200, 50)

button_size = upload_text_button_rect.size
# Answer choice objects
class AnswerChoice:
    @property           
    def name(self): 
        return self._name
    #
    @name.setter   
    def name(self, value):   
        self._name = value  
    @property          
    def correct(self):
        return self._correct
    #
    @correct.setter   
    def correct(self, value):   
        self._correct = value   

    @property           
    def button(self): 
        return self._button
    #
    @button.setter    
    def button(self, value):   
        self._button = value  


# GAMEPLAY VARIABLES
choice_correct = AnswerChoice()
choice_wrong_1 = AnswerChoice()
choice_wrong_2 = AnswerChoice()
max_rounds = 5
turns = 0
global score
score = 0
correct_ans = True
answer_processed = False

# PAGE DRAWING METHODS


def draw_main_page():
    display.blit(bg_image, (0, 0))

    mouse_pos = pygame.mouse.get_pos()
    if upload_text_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display, button_hover_color, upload_text_button_rect)
    else:
        pygame.draw.rect(display, button_color, upload_text_button_rect)
    
    # Draw button text
    font = pygame.font.Font(None, 36)
    text = font.render("Upload Text", True, WHITE)
    text_rect = text.get_rect(center=upload_text_button_rect.center)
    display.blit(text, text_rect)

    if info_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display, button_hover_color, info_button_rect)
    else:
        pygame.draw.rect(display, (217, 217, 217), info_button_rect)
    
    # Draw button text
    text_info = font.render("Info", True, BLACK)
    text_info_rect = text_info.get_rect(center=info_button_rect.center)
    display.blit(text_info, text_info_rect)

    if begin_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display, button_hover_color, begin_button_rect)
    else:
        pygame.draw.rect(display, button_color, begin_button_rect)

    begin_text = font.render("Begin", True, BLACK)
    begin_text_rect = begin_text.get_rect(center=begin_button_rect.center)
    display.blit(begin_text, begin_text_rect)

def draw_task_bar():
    bar_end = 550 * ((score)/max_rounds) -10
    pygame.draw.rect(display, DARK_GREEN, (290, 20, 550, 35))
    pygame.draw.rect(display, GREEN, (297, 27, bar_end, 22))
    pygame.draw.rect(display, BLACK, ((297 + bar_end), 20, 6, 35))
    pygame.draw.rect(display, BLACK, ((297 + bar_end), 20, 17, 9))
    pygame.draw.ellipse(display, BLACK, ((280 + bar_end), 43, 25, 20))
    
def draw_question():
    display.blit(question_bg_image, (0, 0))
    font = pygame.font.Font(None, 48)

    mouse_pos = pygame.mouse.get_pos()
    if next1_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display, button_hover_color, next1_button_rect)
    else:
        pygame.draw.rect(display, button_color, next1_button_rect)

    next_text = font.render("Next", True, BLACK)
    next_text_rect = next_text.get_rect(center=next1_button_rect.center)
    display.blit(next_text, next_text_rect)

def draw_info_page():
    display.blit(bg_image, (0, 0))
    display.blit(intro_text_image, (300, 100))

    mouse_pos = pygame.mouse.get_pos()
    if close_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display, button_hover_color, close_button_rect)
    else:
        pygame.draw.rect(display, RED, close_button_rect)
    
    # Draw button text
    font = pygame.font.Font(None, 36)
    close_text = font.render("Close", True, WHITE)
    text_rect = close_text.get_rect(center=close_button_rect.center)
    display.blit(close_text, text_rect)

def upload_page():
    display.blit(bg_image, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    if close_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display, button_hover_color, close_button_rect)
    else:
        pygame.draw.rect(display, RED, close_button_rect)
    pygame.draw.rect(display, box_color, uploadbox,0)
    font = pygame.font.Font(None, 36)
    close_text = font.render("Close", True, WHITE)
    text_rect = close_text.get_rect(center=close_button_rect.center)
    display.blit(close_text, text_rect)
    




def draw_select_fighter_page():
    display.blit(select_fighter_image, (0, 0))  # Use the loading image here
    # Draw button text
    font = pygame.font.Font(None, 36)

    mouse_pos = pygame.mouse.get_pos()
    if next2_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display, button_hover_color, next2_button_rect)
    else:
        pygame.draw.rect(display, button_color, next2_button_rect)
    next_text = font.render("Next", True, BLACK)
    next_text_rect = next_text.get_rect(center=next2_button_rect.center)
    display.blit(next_text, next_text_rect)

def draw_ending_page():
    display.blit(ending_bg_image, (0, 0))

    #button
    font = pygame.font.Font(None, 36)

    mouse_pos = pygame.mouse.get_pos()
    if play_again_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display, button_hover_color, play_again_button_rect)
    else:
        pygame.draw.rect(display, button_color, play_again_button_rect)
    play_again_text = font.render("Play Again", True, BLACK)
    play_again_text_next = play_again_text.get_rect(center=play_again_button_rect.center)
    display.blit(play_again_text, play_again_text_next)

def draw_answer_result_page():
    display.blit(question_bg_image, (0, 0))

    font = pygame.font.Font(None, 36)
    text = font.render("Correct! OR Incorrect!", True, BLACK)
    text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
    display.blit(text, text_rect)

    mouse_pos = pygame.mouse.get_pos()
    if next3_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display, button_hover_color, next3_button_rect)
    else:
        pygame.draw.rect(display, button_color, next3_button_rect)

    next_text = font.render("Next", True, BLACK)
    next_text_rect = next_text.get_rect(center=next3_button_rect.center)
    display.blit(next_text, next_text_rect)

def draw_fight_page():
    display.blit(they_attack_image, (0, 0))

    font = pygame.font.Font(None, 36)

    mouse_pos = pygame.mouse.get_pos()
    if next4_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display, button_hover_color, next4_button_rect)
    else:
        pygame.draw.rect(display, button_color, next4_button_rect)
    next_text = font.render("Next", True, BLACK)
    next_text_rect = next_text.get_rect(center=next4_button_rect.center)
    display.blit(next_text, next_text_rect)

def draw_battle_begins_page():
    display.blit(battle_begins_bg_image, (0, 0))

    font = pygame.font.Font(None, 36)

    mouse_pos = pygame.mouse.get_pos()
    if next5_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display, button_hover_color, next5_button_rect)
    else:
        pygame.draw.rect(display, button_color, next5_button_rect)
    next_text = font.render("Next", True, BLACK)
    next_text_rect = next_text.get_rect(center=next5_button_rect.center)
    display.blit(next_text, next_text_rect)

def draw_text_highlight_page():
    display.blit(question_bg_image, (0, 0))

    font = pygame.font.Font(None, 36)

    mouse_pos = pygame.mouse.get_pos()
    if next6_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display, button_hover_color, next6_button_rect)
    else:
        pygame.draw.rect(display, button_color, next6_button_rect)
    next_text = font.render("Next", True, BLACK)
    next_text_rect = next_text.get_rect(center=next6_button_rect.center)
    display.blit(next_text, next_text_rect)



# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and input_active and current_page == UPLOAD_PAGE:
            if event.key == pygame.K_RETURN:
                texts = user_text
                user_text = ""  # clear after Enter
                current_page = PAGE_MAIN
                
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_page == PAGE_MAIN and begin_button_rect.collidepoint(event.pos):
                print("Begin button clicked!")
                current_page = PAGE_FIGHTER  # Go to second page
                print(current_page)
                diction = fun(text)
                print(diction)

            if current_page == PAGE_MAIN and upload_text_button_rect.collidepoint(event.pos):
                current_page = UPLOAD_PAGE
            if current_page == UPLOAD_PAGE and close_button_rect.collidepoint(event.pos):
                current_page = PAGE_MAIN
            if current_page == UPLOAD_PAGE and uploadbox.collidepoint(event.pos):
                input_active = True
                box_color = box_color_active
            elif current_page == UPLOAD_PAGE:
                input_active = False
                box_color = box_color_inactive

            if current_page == PAGE_MAIN and info_button_rect.collidepoint(event.pos):
                current_page = INFO_PAGE

            if current_page == INFO_PAGE and close_button_rect.collidepoint(event.pos):
                current_page = PAGE_MAIN
            
            if current_page == PAGE_FIGHTER and next2_button_rect.collidepoint(event.pos):
                current_page = PAGE_BATTLE_BEGINS
            if current_page == PAGE_BATTLE_BEGINS and next5_button_rect.collidepoint(event.pos):
                current_page = PAGE_QUESTION

            if current_page == PAGE_QUESTION and next1_button_rect.collidepoint(event.pos):
                current_page = PAGE_ANS
            if current_page == PAGE_ANS and next3_button_rect.collidepoint(event.pos):
                current_page = PAGE_THEY_ATTACK
            if current_page == PAGE_THEY_ATTACK and next4_button_rect.collidepoint(event.pos):
                current_page = PAGE_REDEMPTION
            if current_page == PAGE_TEXT_HIGHLIGHT and next6_button_rect.collidepoint(event.pos):
                current_page = PAGE_REDEMPTION
            if current_page == PAGE_REDEMPTION and next1_button_rect.collidepoint(event.pos):
                current_page = PAGE_ENDING
            if current_page == PAGE_ENDING and play_again_button_rect.collidepoint(event.pos):
                current_page = PAGE_MAIN

    
            
    if current_page == PAGE_MAIN:
        draw_main_page()
    elif current_page == PAGE_FIGHTER:
        draw_select_fighter_page()
    elif current_page == PAGE_BATTLE_BEGINS:
        draw_battle_begins_page()
    elif current_page == PAGE_QUESTION:
        draw_question()
    elif current_page == PAGE_ENDING:
        draw_ending_page()
    elif current_page == PAGE_ANS:
        draw_answer_result_page()
    elif current_page == INFO_PAGE:
        draw_info_page()
    elif current_page == PAGE_TEXT_HIGHLIGHT:
        draw_text_highlight_page()
    elif current_page == PAGE_REDEMPTION:
        draw_question()
    elif current_page == PAGE_THEY_ATTACK:
        draw_fight_page()
    elif current_page == PAGE_YOU_ATTACK:
        draw_fight_page()
    elif current_page == UPLOAD_PAGE:
        upload_page()
        font = pygame.font.Font(None, 36)
        text_surface = font.render(user_text, True, pygame.Color('white'))
        display.blit(text_surface, (uploadbox.x + 10, uploadbox.y + 10))

    pygame.display.flip()

# Quit Pygame
pygame.quit()

