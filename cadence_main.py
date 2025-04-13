import pygame
import random
import time
import math
import sys
#from google import genai
#client = genai.Client(api_key ='')

import json

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("Cats.mp3")  # or .ogg
pygame.mixer.music.play(-1)

# GEMINI API FUNCTION #

# def fun(txt):
#   response = client.models.generate_content(
#       model="gemini-2.0-flash",
#       contents=["generate 5 quiz questions based on this text and return questions and 4 multiple choice as a json file with questions named question and options named options and the answer named answer", txt],
#   )
#   text = response.text
#   text = text[len("```json"):]
#   text = text[:text.index("```")]
#   data= json.loads(text)
#   questions =[]
#   options = []
#   answer= []
#   highlights=[]
#   for i in data:
#     response = client.models.generate_content(
#         model="gemini-2.0-flash",
#         contents=["can you return a sentence directly from this text that contains the answer to" + i['question'],txt]
#         )
#     questions.append(i['question'])
#     options.append(i['options'])
#     answer.append(i['answer'])
#     highlights.append(response.text)

#   return questions,options,answer,highlights

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

current_page = CHOOSE_FIGHTER

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
close_button_rect.topleft = (600, 400)

#UPLOAD
done_upload_button_rect = button_image.get_rect()
done_upload_button_rect.topleft = (700, 400)

#CHOOSE FIGHTER
left_button_rect = button_image.get_rect()
left_button_rect.topleft = (600, 400)
right_button_rect = button_image.get_rect()
right_button_rect.topleft = (500, 400)
continue_fighter_button_rect = button_image.get_rect()
continue_fighter_button_rect.topleft = (400, 400)

#BATTLE BEGINS
continue_battle_button_rect = button_image.get_rect()
continue_battle_button_rect.topleft = (450, 450)

#QUESTION
done_question_button_rect = button_image.get_rect()
done_question_button_rect.topleft = (300, 500)

#ANS_RESULT
done_result_button_rect = button_image.get_rect()
done_result_button_rect.topleft = (450, 500)

#YOU ATTACK
continue_attack_button_rect = button_image.get_rect()
continue_attack_button_rect.topleft = (450, 575)

#REVIEW TEXT
done_review_button_rect = button_image.get_rect()
done_review_button_rect.topleft = (400, 400)

#GAME OVER
stats_button_rect = button_image.get_rect()
stats_button_rect.topleft = (450, 500)
play_again_button_rect = button_image.get_rect()
play_again_button_rect.topleft = (450, 400)

#STATS
done_stats_button_rect = button_image.get_rect()
done_stats_button_rect.topleft = (450, 500)

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
    mouse_pos = pygame.mouse.get_pos()
    #print("Mouse:", mouse_pos)
    #if uploaded:
    #    print("Upload rect:", upload_text_button_rect)
    #else: 
    #    print("begin rect:", begin_button_rect)

    display.blit(bg_image, (0, 0))
    display.blit(title_cloud, (75, 15))

    
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
    mouse_pos = pygame.mouse.get_pos()

    display.blit(bg_image_grey, (0, 0))

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
    mouse_pos = pygame.mouse.get_pos()
    display.blit(bg_image_grey, (0, 0))
    

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
    mouse_pos = pygame.mouse.get_pos()
    global visible_chars, last_update

    display.blit(bg_image, (0, 0))

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
        return air_dino
    if num == 3:
        return water_dino


def draw_choose_fighter():
    mouse_pos = pygame.mouse.get_pos()
    display.blit(bg_image_grey, (0, 0))
    display.blit(choose_fighter_cloud, (75, 15))

    mouse_pos = pygame.mouse.get_pos()    


    triangle_color = (50, 50, 50)
    hover_color = (100, 100, 100)

    sprite = choose_player_sprite(sprite_num)
    enemy_sprite = choose_enemy_sprite(sprite_num)
    enemy_sprite = pygame.transform.flip(enemy_sprite, True, False)
    if sprite == 0:
        temp_sprite = pygame.transform.scale(sprite, (350,350))
        display.blit(temp_sprite, (25, 275))
    elif sprite == 1:
        display.blit(sprite, (50, 300))
    elif sprite == 2:
        display.blit(sprite, (25, 300))
    else:
        display.blit(sprite, (50, 325))
    if enemy_sprite == 0:
        display.blit(enemy_sprite, (700, 300))
    elif enemy_sprite == 1:
        display.blit(enemy_sprite, (725, 325))
    elif enemy_sprite == 2:
        temp_enemy_sprite = pygame.transform.scale(enemy_sprite, (350,350))
        display.blit(temp_enemy_sprite, (700, 300))
    else:
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
    return left_triangle_rect, right_triangle_rect


def draw_battle_begins():
    mouse_pos = pygame.mouse.get_pos()
    display.blit(bg_image, (0, 0))
    display.blit(battle_cloud, (75, 15))

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

selected_answer = -1
def draw_question(question_text = "placeholder", answers = ["placeholder - correct", "placeholder", "placeholder", "placeholder"]):
    global selected_answer
    mouse_pos = pygame.mouse.get_pos()
    display.blit(bg_image_grey, (0, 0))

    font = pygame.font.Font(None, 32)

    inner_box = pygame.Rect(200, 80, 700, 460)
    pygame.draw.rect(display, WHITE, inner_box)  
    pygame.draw.rect(display, (100, 100, 100), inner_box, 2)  
    title_text = font.render("Question:", True, BLACK)
    display.blit(title_text, (inner_box.x + 300, inner_box.y + 20)) 

    render_wrapped_text(question_text, font, BLACK, pygame.Rect(inner_box.x + 20, inner_box.y + 60, 660, 100), display)

    start_y = inner_box.y + 180
    circle_radius = 10

    for i, answer in enumerate(answers):
        y_pos = start_y + i * 60
        circle_center = (inner_box.x + 30, y_pos)

        # Check hover
        answer_rect = pygame.Rect(inner_box.x + 20, y_pos - 15, 600, 30)
        if answer_rect.collidepoint(mouse_pos):
            pygame.draw.circle(display, (150, 150, 150), circle_center, circle_radius + 2)

        # Draw filled if selected
        if selected_answer == i:
            pygame.draw.circle(display, BLACK, circle_center, circle_radius)
        else:
            pygame.draw.circle(display, BLACK, circle_center, circle_radius, 2)

        # Draw the answer text
        answer_text = font.render(answer[turns], True, BLACK)
        display.blit(answer_text, (circle_center[0] + 20, y_pos - 12))


    if done_question_button_rect.collidepoint(mouse_pos):
        display.blit(hover_button_image, done_question_button_rect)
    else:
        display.blit(button_image, done_question_button_rect)

    done_text = font.render("Done", True, BLACK)
    text_rect = done_text.get_rect(center=done_question_button_rect.center)
    display.blit(done_text, text_rect)

    sprite = choose_player_sprite(sprite_num)
    enemy_sprite = choose_enemy_sprite(sprite_num)
    enemy_sprite = pygame.transform.flip(enemy_sprite, True, False)
    display.blit(sprite, (25, 400))
    display.blit(enemy_sprite, (750, 400))

def draw_review(review_quote = "placeholder"):
    global selected_answer
    mouse_pos = pygame.mouse.get_pos()
    display.blit(bg_image_grey, (0, 0))
    
    font = pygame.font.Font(None, 32)
    inner_box = pygame.Rect(200, 80, 700, 460)
    pygame.draw.rect(display, WHITE, inner_box)  
    pygame.draw.rect(display, (100, 100, 100), inner_box, 2)  
    title_text = font.render("Text To Review:", True, BLACK)
    display.blit(title_text, (inner_box.x + 300, inner_box.y + 20)) 
    
    render_wrapped_text(review_quote, font, BLACK, pygame.Rect(inner_box.x + 20, inner_box.y + 60, 660, 100), display)
 
    if done_review_button_rect.collidepoint(mouse_pos):
        display.blit(hover_button_image, done_review_button_rect)
    else:
        display.blit(button_image, done_review_button_rect)
 
    done_text = font.render("Done", True, BLACK)
    text_rect = done_text.get_rect(center=done_review_button_rect.center)
    display.blit(done_text, text_rect)
 
    sprite = choose_player_sprite(sprite_num)
    enemy_sprite = choose_enemy_sprite(sprite_num)
    enemy_sprite = pygame.transform.flip(enemy_sprite, True, False)
    display.blit(sprite, (25, 400))
    display.blit(enemy_sprite, (750, 400))
    

def draw_result():
    mouse_pos = pygame.mouse.get_pos()
    display.blit(bg_image_grey, (0, 0))

    flipped_dino = pygame.transform.flip(fire_dino, True, False)
    temp_fire = pygame.transform.scale(flipped_dino, (200, 200))
    display.blit(temp_fire, (900, 350))

    temp_water = pygame.transform.scale(water_dino, (200, 200))
    display.blit(temp_water, (0, 300))

    font = pygame.font.Font(None, 36)

    result_rect = pygame.Rect(200, 100, 700, 500)  
    pygame.draw.rect(display, (255, 255, 255), result_rect) 
    pygame.draw.rect(display, (0, 0, 0), result_rect, 2)   
    result_text = ""
    if correct_ans:
        display.blit(correct_sprite, (350, 125))
        result_text = "Correct Answer!"
    else:
        display.blit(incorrect_sprite, (350, 125))
        result_text = "erm actually..."

    render_wrapped_text(result_text, font, (0, 0, 0), result_rect, display)

    if done_result_button_rect.collidepoint(mouse_pos):
        display.blit(hover_button_image, done_result_button_rect)
    else:
        display.blit(button_image, done_result_button_rect)
    
    # Draw button text
    close_text = font.render("Done", True, BLACK)
    close_text_rect = close_text.get_rect(center=done_result_button_rect.center)
    display.blit(close_text, close_text_rect)

def draw_attack():
    global attacked
    display.blit(bg_image_grey, (0, 0))

    mouse_pos = pygame.mouse.get_pos()
    font = pygame.font.Font(None, 36)
    
    flipped_dino = pygame.transform.flip(fire_dino, True, False)
    display.blit(flipped_dino, (700, 325))

    display.blit(water_dino, (100, 300))

    if continue_attack_button_rect.collidepoint(mouse_pos):
        display.blit(hover_button_image, continue_attack_button_rect)
    else:
        display.blit(button_image, continue_attack_button_rect)
    
    # Draw button text
    text_info = font.render("Continue", True, BLACK)
    continue_rect = text_info.get_rect(center=continue_attack_button_rect.center)
    display.blit(text_info, continue_rect)
    if not attacked: 
        if correct_ans:
            clock = pygame.time.Clock()
            start_pos = (150, 300)
            end_pos = (650, 300)
            duration = 120
            frame = 0

            while frame < duration:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                t = frame / duration
                x = int(start_pos[0] * (1 - t) + end_pos[0] * t)
                y = int(start_pos[1] * (1 - t) + end_pos[1] * t)

                # Redraw everything
                display.blit(bg_image_grey, (0, 0))
                flipped_dino = pygame.transform.flip(fire_dino, True, False)
                display.blit(flipped_dino, (700, 325))
                display.blit(water_dino, (100, 300))

                if continue_attack_button_rect.collidepoint(mouse_pos):
                    display.blit(hover_button_image, continue_attack_button_rect)
                else:
                    display.blit(button_image, continue_attack_button_rect)

                # Only draw bubbles during animation
                display.blit(bubbles, (x, y))
                
                text_info = font.render("Continue", True, BLACK)
                continue_rect = text_info.get_rect(center=continue_attack_button_rect.center)
                display.blit(text_info, continue_rect)

                pygame.display.update()
                clock.tick(60)
                frame += 1

            # 🧹 Cleanup: Final frame with no bubbles
            display.blit(bg_image_grey, (0, 0))
            flipped_dino = pygame.transform.flip(fire_dino, True, False)
            display.blit(flipped_dino, (700, 325))
            display.blit(water_dino, (100, 300))

            if continue_attack_button_rect.collidepoint(mouse_pos):
                display.blit(hover_button_image, continue_attack_button_rect)
            else:
                display.blit(button_image, continue_attack_button_rect)

            text_info = font.render("Continue", True, BLACK)
            continue_rect = text_info.get_rect(center=continue_attack_button_rect.center)
            display.blit(text_info, continue_rect)

            pygame.display.update()

        else:
            clock = pygame.time.Clock()
            start_pos = (650, 300)
            end_pos = (150, 300)
            duration = 120
            frame = 0

            while frame < duration:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                t = frame / duration
                x = int(start_pos[0] * (1 - t) + end_pos[0] * t)
                y = int(start_pos[1] * (1 - t) + end_pos[1] * t)

                # Redraw everything
                display.blit(bg_image_grey, (0, 0))
                flipped_dino = pygame.transform.flip(fire_dino, True, False)
                display.blit(flipped_dino, (700, 325))
                display.blit(water_dino, (100, 300))

                if continue_attack_button_rect.collidepoint(mouse_pos):
                    display.blit(hover_button_image, continue_attack_button_rect)
                else:
                    display.blit(button_image, continue_attack_button_rect)

                text_info = font.render("Continue", True, BLACK)
                continue_rect = text_info.get_rect(center=continue_attack_button_rect.center)
                display.blit(text_info, continue_rect)

                # Only draw bubbles during animation
                display.blit(meatball, (x, y))

                pygame.display.update()
                clock.tick(60)
                frame += 1

            # 🧹 Cleanup: Final frame with no bubbles
            display.blit(bg_image_grey, (0, 0))
            flipped_dino = pygame.transform.flip(fire_dino, True, False)
            display.blit(flipped_dino, (700, 325))
            display.blit(water_dino, (100, 300))

            if continue_attack_button_rect.collidepoint(mouse_pos):
                display.blit(hover_button_image, continue_attack_button_rect)
            else:
                display.blit(button_image, continue_attack_button_rect)

            text_info = font.render("Continue", True, BLACK)
            continue_rect = text_info.get_rect(center=continue_attack_button_rect.center)
            display.blit(text_info, continue_rect)

            pygame.display.update()
    attacked = True

def draw_stats():
    display.blit(bg_image_grey, (0, 0))

    flipped_dino = pygame.transform.flip(fire_dino, True, False)
    temp_fire = pygame.transform.scale(flipped_dino, (200, 200))
    display.blit(temp_fire, (900, 350))

    temp_water = pygame.transform.scale(water_dino, (200, 200))
    display.blit(temp_water, (0, 300))

    mouse_pos = pygame.mouse.get_pos()
    font = pygame.font.Font(None, 36)

    result_rect = pygame.Rect(200, 100, 700, 500)  
    pygame.draw.rect(display, (255, 255, 255), result_rect) 
    pygame.draw.rect(display, (0, 0, 0), result_rect, 2)

#****** TO DO: Text to Review ******
#quotes = ...
    result_text = ("Stats\n\n" + str(score) + "/5 Questions Correct\n\n\nText to Review:\n\n(quotes)")
    render_wrapped_text(result_text, font, (0, 0, 0), result_rect, display)

    if done_stats_button_rect.collidepoint(mouse_pos):
        display.blit(hover_button_image, done_stats_button_rect)
    else:
        display.blit(button_image, done_stats_button_rect)
    
    # Draw button text
    close_text = font.render("Done", True, BLACK)
    close_text_rect = close_text.get_rect(center=done_stats_button_rect.center)
    display.blit(close_text, close_text_rect)

def draw_game_over():
    display.blit(bg_image, (0, 0))
    if score == 5:
        display.blit(you_win_cloud,  (75, 15))
    else:
        display.blit(you_lose_cloud, (75, 15))

    mouse_pos = pygame.mouse.get_pos()
    font = pygame.font.Font(None, 36)
    
    if stats_button_rect.collidepoint(mouse_pos):
        display.blit(hover_button_image, stats_button_rect)
    else:
        display.blit(button_image, stats_button_rect)

    if play_again_button_rect.collidepoint(mouse_pos):
        display.blit(hover_button_image, play_again_button_rect)
    else:
        display.blit(button_image, play_again_button_rect)
    
    # Draw button text
    text_stats = font.render("Stats", True, BLACK)
    stats_rect = text_stats.get_rect(center=stats_button_rect.center)
    display.blit(text_stats, stats_rect)

    text_again = font.render("Play Again", True, BLACK)
    again_rect = text_again.get_rect(center=play_again_button_rect.center)
    display.blit(text_again, again_rect)

# MAIN LOOP #

running = True
input_active = False
click_blocked = False
generating_screen_start_time = None
attacked = False
while running:
    if click_blocked:
        pygame.event.clear(pygame.MOUSEBUTTONDOWN)  # clear stale clicks
        click_blocked = False
        continue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and current_page == UPLOAD:
                
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_page == HOME_SCREEN and uploaded == False and upload_text_button_rect.collidepoint(event.pos):
                #print("Clicked Upload!")
                current_page = UPLOAD
                clicked_blocked = True

            if current_page == HOME_SCREEN and info_button_rect.collidepoint(event.pos):
                current_page = INFO
                clicked_blocked = True

            if current_page == HOME_SCREEN and uploaded == True and begin_button_rect.collidepoint(event.pos):
                current_page = GENERATING_QUESTIONS
                generating_screen_start_time = pygame.time.get_ticks()
                question,options,answer,highlights = fun(user_text)
                clicked_blocked = True

            if current_page == UPLOAD and done_upload_button_rect.collidepoint(event.pos):
                uploaded = True
                current_page = HOME_SCREEN
                clicked_blocked = True

            if current_page == INFO and close_button_rect.collidepoint(event.pos):
                current_page = HOME_SCREEN
                clicked_blocked = True

            if current_page == CHOOSE_FIGHTER and continue_fighter_button_rect.collidepoint(event.pos):
                current_page = BATTLE_BEGINS
                clicked_blocked = True

            if current_page == CHOOSE_FIGHTER and left_button_rect.collidepoint(event.pos):
                sprite_num -= 1
                if sprite_num < 0:
                    sprite_num = 3

            if current_page == CHOOSE_FIGHTER and right_button_rect.collidepoint(event.pos):
                if sprite_num > 3:
                    sprite_num = 0

            if current_page == BATTLE_BEGINS and continue_battle_button_rect.collidepoint(event.pos):
                current_page = QUESTION
                clicked_blocked = True

            if current_page == QUESTION and done_question_button_rect.collidepoint(event.pos):
                turns += 1
                current_page = ANS_RESULT
                clicked_blocked = True

            if current_page == ANS_RESULT and done_result_button_rect.collidepoint(event.pos):
                if turns > 4:
                    current_page = GAME_OVER
                else:
                    current_page = ATTACK
                clicked_blocked = True

            if current_page == ATTACK and continue_attack_button_rect.collidepoint(event.pos):
                if turns > 4:
                    current_page = GAME_OVER
                    clicked_blocked = True
                elif correct_ans:
                    score += 1
                    current_page = QUESTION
                    clicked_blocked = True
                else:
                    current_page = REVIEW_TEXT
                    clicked_blocked = True

            if current_page == REVIEW_TEXT and done_review_button_rect.collidepoint(event.pos):
                if turns > 4:
                    current_page = GAME_OVER
                    clicked_blocked = True
                else:
                    current_page = QUESTION
                    clicked_blocked = True

            if current_page == GAME_OVER and stats_button_rect.collidepoint(event.pos):
                current_page = STATS
                clicked_blocked = True

            if current_page == GAME_OVER and play_again_button_rect.collidepoint(event.pos):
                uploaded = False
                turns = 0
                score = 0
                sprite_num = 0
                current_page = HOME_SCREEN
                clicked_blocked = True

            if current_page == STATS and done_stats_button_rect.collidepoint(event.pos):
                current_page = GAME_OVER
                clicked_blocked = True


        #play again -- uploaded is false
    if current_page == GENERATING_QUESTIONS and generating_screen_start_time is not None:
        if pygame.time.get_ticks() - generating_screen_start_time >= 3000:  # 3 seconds
            current_page = CHOOSE_FIGHTER
            generating_screen_start_time = None  # reset timer
            click_blocked = True

    if current_page == HOME_SCREEN:
        draw_home_screen()
    elif current_page == INFO:
        draw_info()
    elif current_page == UPLOAD:
        draw_upload()
        font = pygame.font.Font(None, 36)
        text_surface = font.render(user_text, True, pygame.Color('white'))
        display.blit(text_surface, (uploadbox.x + 10, uploadbox.y + 10))
    elif current_page == HOME_SCREEN_2:
        draw_home_screen()
    elif current_page == GENERATING_QUESTIONS:
        draw_generating_questions()
    elif current_page == CHOOSE_FIGHTER:
        left_triangle_rect, right_triangle_rect = draw_choose_fighter()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if left_triangle_rect.collidepoint(event.pos):
                sprite_num -= 1
            if sprite_num < 0:
                sprite_num = 3

            if right_triangle_rect.collidepoint(event.pos):
                sprite_num += 1
            if sprite_num > 3:
                sprite_num = 0

    elif current_page == BATTLE_BEGINS:
        draw_battle_begins()
    elif current_page == QUESTION:
        draw_question(question[turns], options) 
        attacked = False
    elif current_page == ANS_RESULT:
        draw_result()
    elif current_page == ATTACK:
        draw_attack() #need status of who was correct last
    elif current_page == REVIEW_TEXT:
        draw_review(highlights)
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
    
    

