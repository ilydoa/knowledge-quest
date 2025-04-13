import pygame
import random
import time
from google import genai
client = genai.Client(api_key ='AIzaSyA76gxgHIN4kRsPMb_6KhLNO_Vq05W5tXE')

import json

# GEMINI API FUNCTION #

def fun(txt):
  response = client.models.generate_content(
      model="gemini-2.0-flash",
      contents=["generate 5 quiz questions based on this text and return questions and 4 multiple choice as a json file with questions named question and options named options and the answer named answer", txt],
  )
  text = response.text
  text = text[len("```json"):]
  text = text[:text.index("```")]
  data= json.loads(text)
  questions =[]
  options = []
  answer= []
  highlights=[]
  for i in data:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=["can you return a sentence directly from this text that contains the answer to" + i['question'],txt]
        )
    questions.append(i['question'])
    options.append(i['options'])
    answer.append(i['answer'])
    highlights.append(response.text)

  return questions,options,answer,highlights

text = "One of the first organisms that humans domesticated was yeast. In 2011, while excavating an old graveyard in an Armenian cave, scientists discovered a 6,000 year-old winery, complete with a wine press, fermentation vessels, and even drinking cups. This winery was a major technological innovation that required understanding how to control Sacharomyces, the genus of yeast used in alcohol and bread production."

pygame.init()
pygame.mixer.init()

# GEMINI TEXT BOX #

user_text = ""
texts = ""
box_color_active = pygame.Color('lightskyblue3')
box_color_inactive = pygame.Color('gray15')
box_color = box_color_inactive

# COLORS #

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (129, 167, 144)
DARK_GREEN = (36,130,72)
RED = (255, 0, 0)


# LOADING IMAGES FOR SPRITES AND BACKGROUND #

window_size = (1100, 700)
display = pygame.display.set_mode(window_size)

bg_image = pygame.image.load('final_sprites/forest_background_bigger.png')
bg_image = pygame.transform.scale(bg_image, window_size)

bg_image_grey = pygame.image.load('final_sprites/forest_background_grey.png')
bg_image_grey = pygame.transform.scale(bg_image_grey, window_size)

title_cloud = pygame.image.load('final_sprites/knowlege_quest_cloud.png')
title_cloud = pygame.transform.scale(title_cloud, (1000, 700))

choose_fighter_cloud = pygame.image.load('final_sprites/choose_fighter_cloud.png')
choose_fighter_cloud = pygame.transform.scale(choose_fighter_cloud, (1000, 700))

battle_cloud = pygame.image.load('final_sprites/battle_begins_cloud.png')
battle_cloud = pygame.transform.scale(battle_cloud, (1000, 700))

you_win_cloud = pygame.image.load('final_sprites/you_win_cloud.png')
you_win_cloud = pygame.transform.scale(you_win_cloud, (1000, 700))

you_lose_cloud = pygame.image.load('final_sprites/you_lose_cloud.png')
you_lose_cloud = pygame.transform.scale(you_lose_cloud, (1000, 700))

button_image = pygame.image.load('final_sprites/button2.png')
button_image = pygame.transform.scale(button_image, (200, 70))

hover_button_image = pygame.image.load('final_sprites/hover_button.png')
hover_button_image = pygame.transform.scale(hover_button_image, (200, 70))

empty_cloud = pygame.image.load('final_sprites/cloud.png')
empty_cloud = pygame.transform.scale(empty_cloud, (700, 500))

earth_dino = pygame.image.load('final_sprites/earthDino.png')
earth_dino = pygame.transform.scale(earth_dino, (400, 400))

fire_dino = pygame.image.load('final_sprites/fireDino.png')
fire_dino = pygame.transform.scale(fire_dino, (275, 275))

air_dino = pygame.image.load('final_sprites/airDino.png')
air_dino = pygame.transform.scale(air_dino, (400, 400))

water_dino = pygame.image.load('final_sprites/waterDino.png')
water_dino = pygame.transform.scale(water_dino, (300, 300))

incorrect_sprite = pygame.image.load('final_sprites/ermActually.png')
incorrect_sprite = pygame.transform.scale(incorrect_sprite, (400, 400))

correct_sprite = pygame.image.load('final_sprites/happy.png')
correct_sprite = pygame.transform.scale(correct_sprite, (400, 400))

meatball = pygame.image.load('final_sprites/meatball.png')
meatball = pygame.transform.scale(meatball, (200, 200))

tornado = pygame.image.load('final_sprites/tornado.png')
tornado = pygame.transform.scale(tornado, (200, 200))

bees = pygame.image.load('final_sprites/bees.png')
bees = pygame.transform.scale(bees, (200, 200))

bubbles = pygame.image.load('final_sprites/bubbles.png')
bubbles = pygame.transform.scale(bubbles, (200, 200))

# PAGE STATES #

HOME_SCREEN = 0
HOME_SCREEN_2 = 1
INFO = 3
UPLOAD = 4
GENERATING_QUESTIONS = 5
CHOOSE_FIGHTER = 6
BATTLE_BEGINS = 7
QUESTION = 8
ANS_RESULT = 9
ATTACK = 10
REVIEW_TEXT = 11
GAME_OVER = 12
STATS = 13

current_page = BATTLE_BEGINS

# BUTTONS #

#HOME SCREEN
upload_text_button_rect = button_image.get_rect()
upload_text_button_rect.topleft = (450, 400)
info_button_rect = button_image.get_rect()
info_button_rect.topleft = (450, 500)
begin_button_rect = button_image.get_rect()
begin_button_rect.topleft = (450, 400)

#INFO
close_button_rect = button_image.get_rect()
close_button_rect.topleft = (450, 575)

#UPLOAD
done_upload_button_rect = button_image.get_rect()
done_upload_button_rect.topleft = (450, 575)

#CHOOSE FIGHTER
left_button_rect = button_image.get_rect()
left_button_rect.topleft = (600, 400)
right_button_rect = button_image.get_rect()
right_button_rect.topleft = (500, 400)
continue_fighter_button_rect = button_image.get_rect()
continue_fighter_button_rect.topleft = (450, 575)

#BATTLE BEGINS
continue_battle_button_rect = button_image.get_rect()
continue_battle_button_rect.topleft = (450, 450)

#QUESTION
done_question_button_rect = button_image.get_rect()
done_question_button_rect.topleft = (300, 500)

#ANS_RESULT
done_result_button_rect = button_image.get_rect()
done_result_button_rect.topleft = (300, 600)

#YOU ATTACK
continue_attack_button_rect = button_image.get_rect()
continue_attack_button_rect.topleft = (300, 700)

#REVIEW TEXT
done_review_button_rect = button_image.get_rect()
done_review_button_rect.topleft = (400, 400)

#GAME OVER
stats_button_rect = button_image.get_rect()
stats_button_rect.topleft = (500, 400)
play_again_button_rect = button_image.get_rect()
play_again_button_rect.topleft = (600, 400)

#STATS
done_stats_button_rect = button_image.get_rect()
done_stats_button_rect.topleft = (700, 400)

button_size = upload_text_button_rect.size


uploadbox = pygame.Rect(200, 50, 700, 500)
# ANSWER CHOICE CLASS #

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


# GAMEPLAY VARIABLES #

choice_correct = AnswerChoice()
choice_wrong_1 = AnswerChoice()
choice_wrong_2 = AnswerChoice()
choice_wrong_3 = AnswerChoice()

max_rounds = 5
turns = 0
global score
score = 0

sprite_num = 0

correct_ans = True
answer_processed = False
uploaded = False

# PAGE DRAWING METHODS #

def draw_home_screen():
    display.blit(bg_image, (0, 0))
    display.blit(title_cloud, (75, 15))

    mouse_pos = pygame.mouse.get_pos()
    font = pygame.font.Font(None, 36)

    if uploaded:
        if begin_button_rect.collidepoint(mouse_pos):
            display.blit(hover_button_image, begin_button_rect)
        else:
            display.blit(button_image, begin_button_rect)

        begin_text = font.render("Begin", True, BLACK)
        begin_text_rect = begin_text.get_rect(center=begin_button_rect.center)
        display.blit(begin_text, begin_text_rect)
    else:
        if upload_text_button_rect.collidepoint(mouse_pos):
            display.blit(hover_button_image, upload_text_button_rect)
        else:
            display.blit(button_image, upload_text_button_rect)
    
    # Draw button text
        font = pygame.font.Font(None, 36)
        text = font.render("Upload Text", True, BLACK)
        text_rect = text.get_rect(center=upload_text_button_rect.center)
        display.blit(text, text_rect)
    
    if info_button_rect.collidepoint(mouse_pos):
        display.blit(hover_button_image, info_button_rect)
    else:
        display.blit(button_image, info_button_rect)
    
    # Draw button text
    text_info = font.render("Info", True, BLACK)
    text_info_rect = text_info.get_rect(center=info_button_rect.center)
    display.blit(text_info, text_info_rect)

def render_wrapped_text(text, font, color, rect, surface, line_spacing=5):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        test_surface = font.render(test_line, True, color)
        if test_surface.get_width() <= rect.width - 20:  # 20 for padding
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)  # last line

    y = rect.y + 20  # top padding
    for line in lines:
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (rect.x + 20, y))  # left padding
        y += line_surface.get_height() + line_spacing

def draw_info():
    display.blit(bg_image_grey, (0, 0))

    mouse_pos = pygame.mouse.get_pos()
    font = pygame.font.Font(None, 36)

    info_rect = pygame.Rect(200, 100, 700, 500)  
    pygame.draw.rect(display, (255, 255, 255), info_rect) 
    pygame.draw.rect(display, (0, 0, 0), info_rect, 2)   

    info_text = ("Weclome to Knowledge Quest!"
                            "\n\nEver wished you could gamify your readings? This is the game for you!" 
                            "\n\nKnowledge Quest uses Gemini to generate reading comprehension questions based on"
                            "reading assignments players paste in. \n\nHappy studying!")
    render_wrapped_text(info_text, font, (0, 0, 0), info_rect, display)

    if close_button_rect.collidepoint(mouse_pos):
        display.blit(hover_button_image, close_button_rect)
    else:
        display.blit(button_image, close_button_rect)
    
    # Draw button text
    close_text = font.render("Close", True, BLACK)
    close_text_rect = close_text.get_rect(center=close_button_rect.center)
    display.blit(close_text, close_text_rect)

def draw_upload():
    display.blit(bg_image_grey, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    outer_box = pygame.Rect(180, 30, 740, 540) 
    pygame.draw.rect(display, (200, 200, 200), outer_box)   
    pygame.draw.rect(display, BLACK, outer_box, 3)          

    font = pygame.font.Font(None, 36)
    title_text = font.render("Paste text here:", True, BLACK)
    display.blit(title_text, (outer_box.x + 20, outer_box.y + 10)) 

    inner_box = pygame.Rect(200, 80, 700, 460)
    pygame.draw.rect(display, WHITE, inner_box)  
    pygame.draw.rect(display, (100, 100, 100), inner_box, 2)  

    if done_upload_button_rect.collidepoint(mouse_pos):
        display.blit(hover_button_image, done_upload_button_rect)
    else:
        display.blit(button_image, done_upload_button_rect)

    done_text = font.render("Done", True, BLACK)
    text_rect = done_text.get_rect(center=done_upload_button_rect.center)
    display.blit(done_text, text_rect)


full_message = "Generating questions . . ."
visible_chars = 0
last_update = pygame.time.get_ticks()
char_delay = 100  

def draw_generating_questions():
    global visible_chars, last_update

    display.blit(bg_image, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    text_box = pygame.Rect(150, 250, 700, 100)
    pygame.draw.rect(display, WHITE, text_box)
    pygame.draw.rect(display, BLACK, text_box, 2)

    current_time = pygame.time.get_ticks()
    if visible_chars < len(full_message) and current_time - last_update > char_delay:
        visible_chars += 1
        last_update = current_time

    font = pygame.font.Font(None, 36)
    current_text = full_message[:visible_chars]
    text_surface = font.render(current_text, True, BLACK)
    display.blit(text_surface, (text_box.x + 20, text_box.y + 30))

def choose_player_sprite(num):
    if num == 0:
        return air_dino
    if num == 1:
        return water_dino
    if num == 2:
        return earth_dino
    if num == 3:
        return fire_dino
    
def choose_enemy_sprite(num):
    if num == 0:
        return earth_dino
    if num == 1:
        return fire_dino
    if num == 2:
        return earth_dino
    if num == 3:
        return water_dino


def draw_choose_fighter():
    display.blit(bg_image_grey, (0, 0))
    display.blit(choose_fighter_cloud, (75, 15))

    mouse_pos = pygame.mouse.get_pos()    


    triangle_color = (50, 50, 50)
    hover_color = (100, 100, 100)

    sprite = choose_player_sprite(sprite_num)
    enemy_sprite = choose_enemy_sprite(sprite_num)
    enemy_sprite = pygame.transform.flip(enemy_sprite, True, False)
    display.blit(sprite, (50, 300))
    display.blit(enemy_sprite, (700, 300))

    sprite_x, sprite_y = 50, 300
    sprite_width, sprite_height = sprite.get_width(), sprite.get_height()


    center_y = sprite_y + sprite_height // 2

    left_triangle = [
        (sprite_x - 2, center_y - 25),
        (sprite_x - 2, center_y + 25),
        (sprite_x - 22, center_y)
    ]

    right_triangle = [
        (sprite_x + sprite_width + 2, center_y - 25),
        (sprite_x + sprite_width + 2, center_y + 25),
        (sprite_x + sprite_width + 22, center_y)
    ]


    left_triangle_rect = pygame.Rect(
        min(p[0] for p in left_triangle),
        min(p[1] for p in left_triangle),
        max(p[0] for p in left_triangle) - min(p[0] for p in left_triangle),
        max(p[1] for p in left_triangle) - min(p[1] for p in left_triangle)
    )

    right_triangle_rect = pygame.Rect(
        min(p[0] for p in right_triangle),
        min(p[1] for p in right_triangle),
        max(p[0] for p in right_triangle) - min(p[0] for p in right_triangle),
        max(p[1] for p in right_triangle) - min(p[1] for p in right_triangle)
    )
    

    if left_triangle_rect.collidepoint(mouse_pos):
        pygame.draw.polygon(display, hover_color, left_triangle)
    else:
        pygame.draw.polygon(display, triangle_color, left_triangle)

    if right_triangle_rect.collidepoint(mouse_pos):
        pygame.draw.polygon(display, hover_color, right_triangle)
    else:
        pygame.draw.polygon(display, triangle_color, right_triangle)

    font = pygame.font.Font(None, 36)

    if continue_fighter_button_rect.collidepoint(mouse_pos):
        display.blit(hover_button_image, continue_fighter_button_rect)
    else:
        display.blit(button_image, continue_fighter_button_rect)

    continue_fighter_text = font.render("Continue", True, BLACK)
    continue_fighter_text_rect = continue_fighter_text.get_rect(center=continue_fighter_button_rect.center)
    display.blit(continue_fighter_text, continue_fighter_text_rect)


def draw_battle_begins():
    display.blit(bg_image, (0, 0))
    display.blit(battle_cloud, (75, 15))

    mouse_pos = pygame.mouse.get_pos()
    font = pygame.font.Font(None, 36)
    
    flipped_dino = pygame.transform.flip(fire_dino, True, False)
    display.blit(flipped_dino, (700, 325))

    display.blit(water_dino, (100, 300))

    if continue_battle_button_rect.collidepoint(mouse_pos):
        display.blit(hover_button_image, continue_battle_button_rect)
    else:
        display.blit(button_image, continue_battle_button_rect)
    
    # Draw button text
    text_info = font.render("Continue", True, BLACK)
    continue_rect = text_info.get_rect(center=continue_battle_button_rect.center)
    display.blit(text_info, continue_rect)

def draw_question():
    pass

def draw_result():
    pass

def draw_attack():
    pass

def draw_review():
    pass

def draw_game_over():
    pass

def draw_stats():
    pass

# MAIN LOOP #

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if other
    
    if current_page == HOME_SCREEN:
        draw_home_screen()
    elif current_page == INFO:
        draw_info()
    elif current_page == UPLOAD:
        draw_upload()
    elif current_page == HOME_SCREEN_2:
        draw_home_screen()
    elif current_page == GENERATING_QUESTIONS:
        draw_generating_questions()
    elif current_page == CHOOSE_FIGHTER:
        draw_choose_fighter()
    elif current_page == BATTLE_BEGINS:
        draw_battle_begins()
    elif current_page == QUESTION:
        draw_question() #
    elif current_page == ANS_RESULT:
        draw_result()
    elif current_page == ATTACK:
        draw_attack() #need status of who was correct last
    elif current_page == REVIEW_TEXT:
        draw_review()
    elif current_page == GAME_OVER:
        draw_game_over()
    elif current_page == STATS:
        draw_stats()
    
    pygame.display.flip()
#question,options,answer,highlights = fun(user_text)
    

#if event.type == pygame.MOUSEBUTTONDOWN:
#    if left_triangle_rect.collidepoint(event.pos):
#        sprite_num = (sprite_num - 1) % total_sprites
#    elif right_triangle_rect.collidepoint(event.pos):
#        sprite_num = (sprite_num + 1) % total_sprites

# Quit pygame
pygame.quit()
    
    

