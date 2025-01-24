#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 03-Dec-24

@author: apurv
"""
import random

import dae_progfa_lib as pfe
from dae_progfa_lib import ShapeMode, MouseButton
from dae_progfa_lib import MouseButton
import math
from pygame.math import Vector2

from enum import Enum

# Create an instance of ProgfaEngine and set window size (width, height):
engine = pfe.ProgfaEngine(1280, 720)

# Set the frame rate to x frames per second:
engine.set_fps(60)

class Game(Enum):
    MENU = 0
    LEVEL_SELECT = 1
    GAMEPLAY = 2
    DEAD = 3
    WON = 4
    CHEAT_MODE = 5
current_state = Game.MENU


list_background_images = []
list_ground_plane = []
list_grass = []

list_char_l = []  # Char facing left side
list_char_r = []  # Char facing right side

list_enemy_l = [] # Enemy 3 going to left side
list_enemy_r = [] # Enemy 1 going to right side
list_enemy_r_2 = [] # Enemy 2 going to right side

list_enemy_strike_r = []
list_enemy_strike_l = []
state = "LEFT"

enemy_walk_cycle_counter = 0
enemy_walk_cycle_wait_counter = 0

enemy_walk_cycle_counter_2 = 0
enemy_walk_cycle_wait_counter_2 = 0

strike_counter = 0
strike_wait_counter = 0

pos_x = 0
pos_x_2 = 0
pos_x_3 = engine.width

speed_x = 5
speed_x_2 = 5
speed_x_3 = -5

counter = 0
wait_counter = 0

enemy_r = []

list_shoot_img =[]

list_decorations = []
#
# ground_plane_1 = engine.load_image("Resources/ground_plane/ground_plane_1.png")
# ground_plane_2 = engine.load_image("Resources/ground_plane/ground_plane_2.png")

# grass_1 = engine.load_image("Resources/grass/grass_1.png")
# grass_2 = engine.load_image("Resources/grass/grass_2.png")
# grass_3 = engine.load_image("Resources/grass/grass_3.png")

rock_1 = engine.load_image("Resources/rocks/rock_1.png")
rock_2 = engine.load_image("Resources/rocks/rock_2.png")
rock_3 = engine.load_image("Resources/rocks/rock_3.png")

list_char_heart = []
difficulty = ""
difficulty_flag = False

def setup():
    """
    Only executed ONCE (at the start); use to load files and initialize.
    """
    global list_enemy_r_2, list_enemy_strike_r_2, enemy_1
    # Background images loaded
    for number in range(1, 4):
        background_layers = engine.load_image(f"Resources/background/background_layer_{number}.png")
        list_background_images.append(background_layers)
    print(len(list_background_images))

    # Ground planes are loaded
    for number in range(1,5):
        ground_plane =  engine.load_image(f"Resources/ground_plane/ground_plane_{number}.png")
        list_ground_plane.append(ground_plane)
    print(len(list_ground_plane))

    # Grass are loaded
    for number in range(1,4):
        grass = engine.load_image(f"Resources/grass/grass_{number}.png")
        list_grass.append(grass)
    print(len(list_grass))

    # Character is loaded

    char_r = engine.load_image(f"Resources/character/right_movement/pos_1_R.png")
    char_l = engine.load_image(f"Resources/character/left_movement/pos_1_L.png")
    list_char_l.append(char_l)
    list_char_r.append(char_r)
    print(len(list_char_r))
    print(len(list_char_l))

    # Font is loaded

    engine.set_font("Resources/font/supermario.ttf")

    # Decorations are loaded:
    fence_1 = engine.load_image("Resources/decorations/fence_1.png")
    list_decorations.append(fence_1)
    fence_2 = engine.load_image("Resources/decorations/fence_2.png")
    list_decorations.append(fence_2)
    sign = engine.load_image("Resources/decorations/sign.png")
    list_decorations.append(sign)
    lamp = engine.load_image("Resources/decorations/lamp.png")
    list_decorations.append(lamp)



    # Char gun's shoot is loaded

    shoot_img = engine.load_image(f"Resources/character/shoot/shoot_1.png")
    list_shoot_img.append(shoot_img)


    # Enemy strike animation is loaded

    for number in range(1,4):
        strike_attack_r = engine.load_image(f"Resources/enemy/right_movement/strike_{number}_R.png")

        list_enemy_strike_r.append(strike_attack_r)
        list_enemy_strike_r_2 = list_enemy_strike_r.copy()

    for number in range(1,4):
        strike_attack_l = engine.load_image(f"Resources/enemy/left_movement/strike_{number}_L.png")

        list_enemy_strike_l.append(strike_attack_l)
        list_enemy_strike_l_2 = list_enemy_strike_l.copy()



    # Enemy 1 is loaded

    for number in range(1,6):
        enemy_r = engine.load_image(f"Resources/enemy/right_movement/pos_{number}_R.png")

        list_enemy_r.append(enemy_r)
        print(f" list enemy r {len(list_enemy_r)}")

        # Enemy 2 is loaded

        list_enemy_r_2 = list_enemy_r.copy()

    # Enemy 3 is loaded:
    for number in range(1,6):
        enemy_l = engine.load_image(f"Resources/enemy/left_movement/pos_{number}_L.png")

        list_enemy_l.append(enemy_l)

        # Enemy 4 is loaded:
        list_enemy_l_2 = list_enemy_l.copy()


    pass

def hearts():
    global list_char_heart, difficulty
    if difficulty == "Easy":
        heart_param = 6
        for number in range(1, heart_param):
            char_heart_img = engine.load_image(f"Resources/character/heart/heart_{number}.png")
            list_char_heart.append(char_heart_img)
            print(f"Length of heart: {list_char_heart}")

    elif difficulty == "Medium":
        heart_param = 5
        for number in range(1, heart_param):
            char_heart_img = engine.load_image(f"Resources/character/heart/heart_{number}.png")
            list_char_heart.append(char_heart_img)

    elif difficulty == "Hard":
        heart_param = 4
        for number in range(1, heart_param):
            char_heart_img = engine.load_image(f"Resources/character/heart/heart_{number}.png")
            list_char_heart.append(char_heart_img)

        pass

def main_menu():
    # Main Menu image is side_loaded
    global current_state

    main_menu_bg_image = engine.load_image("Resources/main_menu/wp7787095-low-poly-landscape-wallpapers.jpg")
    game_name = engine.load_image("Resources/main_menu/cooltext473911308146716.png")

    main_menu_bg_image.draw_fixed_size(0,0,engine.width, engine.height)
    game_name.draw_fixed_size(engine.width/4,engine.height/8,700,700)

    engine.color =88/255,46/255,70/255


    engine.draw_rectangle(engine.width/2 - 100,engine.height -100, 200,50)

    if engine.colliding_pointinrect(engine.mouse_x, engine.mouse_y,engine.width/2 - 100,engine.height -100,200,50):
        engine.outline_color = 1,1,1
    else:
        engine.outline_color = 0,0,0

    engine.color = 1,1,1
    engine.draw_text("PLAY!",engine.width/2 - 20,engine.height -80)

    # Updated code:
    dae_button = engine.load_image("Resources/required_button/button_image.png")
    dae_button.draw_fixed_size(engine.width - 100, 30, 100,40)

    pass



def level_select():
    global difficulty
    main_menu_bg_image = engine.load_image("Resources/main_menu/wp7787095-low-poly-landscape-wallpapers.jpg")
    main_menu_bg_image.draw_fixed_size(0, 0, engine.width, engine.height)


    engine.color =1,1,1
    engine.draw_text("Select Difficulty", engine.width/2 - 75,200)

    if engine.colliding_pointinrect(engine.mouse_x, engine.mouse_y,engine.width/2 - 100,500,200,50):
        engine.outline_color = 1,1,1
        difficulty = "Hard"

    else:
        engine.outline_color = 0,0,0
    engine.color =88/255,46/255,70/255
    engine.draw_rectangle(engine.width/2 - 100,500, 200,50)



    if engine.colliding_pointinrect(engine.mouse_x, engine.mouse_y,engine.width/2 - 100,300,200,50):
         engine.outline_color = 1,1,1
         difficulty = "Easy"

    else:
        engine.outline_color = 0,0,0
    engine.draw_rectangle(engine.width/2 - 100,300, 200,50)



    if engine.colliding_pointinrect(engine.mouse_x, engine.mouse_y,engine.width/2 - 100,400,200,50):
         engine.outline_color = 1,1,1
         difficulty = "Medium"
    else:
        engine.outline_color =0,0,0

    engine.draw_rectangle(engine.width/2 - 100,400, 200,50)

    engine.color =1,1,1
    engine.draw_text("Easy",engine.width/2 - 20, 320)
    engine.draw_text("Medium",engine.width/2 - 30, 420)
    engine.draw_text("Hard",engine.width/2 - 20, 520)

    pass




def draw_background():
    """
    Draws background
    :return:
    """
    for index in range(0,len(list_background_images)):
        list_background_images[index].draw_fixed_size(0,0,engine.width, engine.height)

    # background_layer_2.draw_fixed_size(0,0,engine.width, engine.height)
    # background_layer_3.draw_fixed_size(0,0,engine.width, engine.height)

def draw_ground_plane():
    """
    Draw ground plane
    :return:
    """
    list_ground_plane[0].draw_fixed_size(0,engine.height - 100 ,engine.width/4, engine.height/4)
    list_ground_plane[1].draw_fixed_size(319, engine.height - 100, engine.width / 6, engine.height / 6)
    list_ground_plane[2].draw_fixed_size(430, engine.height - 100, engine.width / 6, engine.height / 6)
    list_ground_plane[3].draw_fixed_size(550, engine.height - 97, engine.width / 4, engine.height / 4)
    list_ground_plane[0].draw_fixed_size(850, engine.height - 100 ,engine.width/4, engine.height/4)
    list_ground_plane[1].draw_fixed_size(1170, engine.height - 100, engine.width / 6, engine.height / 6)



def draw_grass():
    """
    Draw grass
    :return:
    """
    list_grass[0].draw_fixed_size(100, engine.height - engine.height/4 + 73, 20, 20)
    list_grass[1].draw_fixed_size(170, engine.height - engine.height/4 + 73, 20, 20)
    list_grass[1].draw_fixed_size(480, 610, 30, 30)
    list_grass[1].draw_fixed_size(845, 610, 30, 30)
    list_grass[0].draw_fixed_size(1000, 610, 30,30)
    list_grass[1].draw_fixed_size(1100, 610, 30, 30)






def draw_rocks():
    """
    Draw rocks
    :return:
    """
    rock_1.draw_fixed_size(150, engine.height - engine.height/4 + 70, 20, 20)
    rock_2.draw_fixed_size(300, engine.height - engine.height/4 + 71, 20, 20)
    rock_2.draw_fixed_size(535, engine.height - engine.height/4 + 70, 30, 30)

def draw_decorations():
    list_decorations[0].draw_fixed_size(150, 580, 150, 150)
    list_decorations[1].draw_fixed_size(500, 580, 150, 150)
    list_decorations[2].draw_fixed_size(430, 550, 70, 70)
    list_decorations[3].draw_fixed_size(380, 530, 90, 90)
    list_decorations[3].draw_fixed_size(850, 530, 90, 90)




    pass

def draw_character():
    global state
    if state == 'RIGHT':
        list_char_r[0].draw_fixed_size(engine.width/2, engine.height - engine.height/4 - 15, 100,100)

    elif state == 'LEFT':
        list_char_l[0].draw_fixed_size(engine.width/2, engine.height - engine.height/4 - 15, 100,100)



def draw_enemy():
    if len(list_enemy_r) > 0:
        list_enemy_r[enemy_walk_cycle_counter].draw_fixed_size(pos_x, engine.height - engine.height/4 - 15, 100,100)

    if in_game_time_counter() >= 30:
        if len(list_enemy_r_2) > 0:
            list_enemy_r_2[enemy_walk_cycle_counter_2].draw_fixed_size(pos_x_2, engine.height - engine.height / 4 - 15, 100, 100)

    if in_game_time_counter() >= 60:
        if len(list_enemy_l) > 0:
            list_enemy_l[enemy_walk_cycle_counter_3].draw_fixed_size(pos_x_3, engine.height - engine.height / 4 - 15, 100, 100)

enemy_walk_cycle_wait_counter_3 = 0
enemy_walk_cycle_counter_3 = 0

def walk_cycle_enemy(enemy_number):
    global enemy_walk_cycle_counter, enemy_walk_cycle_wait_counter, enemy_walk_cycle_wait_counter_2, enemy_walk_cycle_counter_2, enemy_walk_cycle_wait_counter_3, enemy_walk_cycle_counter_3

    if enemy_number == 1:
        enemy_walk_cycle_wait_counter += 1
        if enemy_walk_cycle_wait_counter > 3:
            enemy_walk_cycle_counter += 1
            if enemy_walk_cycle_counter > 4:
                enemy_walk_cycle_counter = 0
            enemy_walk_cycle_wait_counter = 0

    elif enemy_number == 2:
        enemy_walk_cycle_wait_counter_2 += 1
        if enemy_walk_cycle_wait_counter_2 > 3:
            enemy_walk_cycle_counter_2 += 1
            if enemy_walk_cycle_counter_2 > 4:
                enemy_walk_cycle_counter_2 = 0
            enemy_walk_cycle_wait_counter_2 = 0

    elif enemy_number == 3:
        enemy_walk_cycle_wait_counter_3 += 1
        if enemy_walk_cycle_wait_counter_3 > 3:
            enemy_walk_cycle_counter_3 += 1
            if enemy_walk_cycle_counter_3 > 4:
                enemy_walk_cycle_counter_3 = 0
            enemy_walk_cycle_wait_counter_3 = 0

    pass

def enemy_movement():
    global pos_x, speed_x, pos_x_2, speed_x_2, pos_x_3, speed_x_3

    pos_x += speed_x

    if in_game_time_counter() >= 30:
        pos_x_2 += speed_x_2

    if in_game_time_counter() >= 60:
        pos_x_3 += speed_x_3


def stop_enemy():
    global pos_x, speed_x, enemy_walk_cycle_counter, enemy_walk_cycle_counter_2, speed_x_2, pos_x_2, pos_x_3, speed_x_3, enemy_walk_cycle_counter_3

    if pos_x == engine.width / 2 - 40:
        speed_x = 0
        list_enemy_r.clear()
        enemy_walk_cycle_counter = 0

    if pos_x_2 == engine.width / 2 - 40:
        speed_x_2 = 0
        list_enemy_r_2.clear()
        enemy_walk_cycle_counter_2 = 0

    if pos_x_3 == engine.width / 2 + 40:
        speed_x_3 = 0
        list_enemy_l.clear()
        enemy_walk_cycle_counter_3 = 0


def strike_enemy_counter():
    global strike_counter, strike_wait_counter
    strike_wait_counter += 1
    if strike_wait_counter > 10:
        strike_counter += 1
        if strike_counter > 2:
            strike_counter = 0
        strike_wait_counter = 0
    pass


def enemy_strike():
    global shoot_wait_counter, current_state

    if len(list_enemy_strike_r)>0:
        if pos_x >= engine.width/2 - 40:
            list_enemy_strike_r[strike_counter].draw_fixed_size(pos_x, engine.height - engine.height/4 - 15, 100,100)

            shoot_wait_counter +=1
            if shoot_wait_counter >= 100:
                if len(list_char_heart) > 0:
                    list_char_heart.pop()
                    shoot_wait_counter = 0
                elif len(list_char_heart) == 0:
                    current_state = Game.DEAD
                    print("You Lost")


    if len(list_enemy_strike_r_2) > 0:

        if pos_x_2 >= engine.width/2 - 40:
            list_enemy_strike_r_2[strike_counter].draw_fixed_size(pos_x_2, engine.height - engine.height / 4 - 15, 100, 100)
            shoot_wait_counter += 1
            if shoot_wait_counter >= 100:
                if len(list_char_heart) > 0:
                    list_char_heart.pop()
                    shoot_wait_counter = 0
                elif len(list_char_heart) == 0:
                    current_state = Game.DEAD
                    print("You Loose")

    if len(list_enemy_strike_l) > 0:

         if pos_x_3 <= engine.width / 2 + 40:
            list_enemy_strike_l[strike_counter].draw_fixed_size(pos_x_3, engine.height - engine.height / 4 - 15, 100, 100)
            shoot_wait_counter += 1
            if shoot_wait_counter >= 100:
                if len(list_char_heart) > 0:
                    list_char_heart.pop()
                    shoot_wait_counter = 0
                elif len(list_char_heart) == 0:
                    current_state = Game.DEAD
                    print("You Loose")



            # print("Attack")
def random_word_generator(difficulty):
    """
    A set of easy, medium and hard words
    :return:
    """
    easy_words = {"pit", "cat", "car", "den","map","dig", "bat","sun","pen","dog","jam", "hat","net", "pig"}
    medium_words = {"bound","sense","month","alive","magic","time"}
    hard_words = {"fabricated","jacarandas","ubiquitous","macadamias"}


    tuple_easy_words = tuple(easy_words)
    tuple_med_words = tuple(medium_words)
    tuple_hard_words = tuple(hard_words)

    if difficulty == "Easy":
        return random.choice(tuple_easy_words)
    elif difficulty == "Medium":
        return random.choice(tuple_med_words)
    elif difficulty == "Hard":
        return random.choice(tuple_hard_words)

words = []

def words_fill():
    easy_words = {"pit", "cat", "car", "den", "map", "dig", "bat", "sun", "pen", "dog", "jam", "hat", "net", "pig"}
    medium_words = {"bound", "sense", "month", "alive", "magic", "time"}
    hard_words = {"fabricated", "jacarandas", "ubiquitous", "macadamias"}
    list_easy_words = list(easy_words)
    list_med_words = list(medium_words)
    list_hard_words = list(hard_words)

    words.extend(list_easy_words)
    words.extend(list_med_words)
    words.extend(list_hard_words)
    words.insert(0,"DAE")
    print(words)
words_fill()

random_word_1 = None
random_word_2 = None
random_word_3 = None


# if difficulty_flag:
#     random_word_1 = random_word_generator(difficulty)
#     random_word_2 = random_word_generator(difficulty)
#     random_word_3 = random_word_generator(difficulty)

def setup_random_words(difficulty):
    global random_word_1, random_word_2, random_word_3

    random_word_1 = random_word_generator(difficulty)
    random_word_2 = random_word_generator(difficulty)
    random_word_3 = random_word_generator(difficulty)

random_word_state_1 = True
random_word_state_2 = True
random_word_state_3 = True

def display_random_word():

    global input_active, user_input_buffer
    if random_word_state_1:
        engine.draw_text(random_word_1, pos_x, engine.height - engine.height/4 - 30)
    if random_word_state_2:
        if in_game_time_counter() >= 30:
            engine.draw_text(random_word_2, pos_x_2, engine.height - engine.height/4 - 30)
    if random_word_state_3:
        if in_game_time_counter() >= 60:
            engine.draw_text(random_word_3, pos_x_3, engine.height - engine.height / 4 - 15)

    if input_active and len(user_input) >1:
        engine.draw_text(f"Your input: {user_input}", engine.width / 2, engine.height / 2 + 50)


input_active = False
user_input_buffer = []
user_input = []

shoot_animation_active = ""

enemy_1 = 1
enemy_2 = 1
enemy_3 = 1

incorrect_words_count = []

def correct_random_word_trigger():
    global input_active, user_input_buffer, state, user_input, random_word_state_1, random_word_state_2, list_enemy_r_2, list_enemy_strike_r, list_enemy_strike_r_2,shoot_animation_active, shoot_wait_counter, random_word_state_3, list_enemy_l, list_enemy_strike_l, enemy_1, enemy_2, enemy_3
    input_active = True
    print(f"Type the word shown: {random_word_1}")

    if input_active:

        if engine.key == "BACKSPACE":
            # Remove the string
            user_input = ""
            user_input_buffer.clear()

        elif engine.key == "ENTER":
            if random_word_1 == user_input:
                print("Correct")
                enemy_1 = 0
                user_input = ""
                user_input_buffer.clear()
                random_word_state_1 = False
                list_enemy_r.clear()
                list_enemy_strike_r.clear()



            if random_word_2 == user_input:
                print("Correct")
                enemy_2 = 0
                user_input = ""
                user_input_buffer.clear()
                random_word_state_2 = False
                list_enemy_r_2.clear()
                list_enemy_strike_r_2.clear()

            if random_word_3 == user_input:
                print("Correct")
                enemy_3 = 0
                user_input = ""
                user_input_buffer.clear()
                random_word_state_3 = False
                list_enemy_l.clear()
                list_enemy_strike_l.clear()



            else:
                incorrect = "Incorrect"
                print(incorrect)
                incorrect_words_count.append(incorrect)

                # input_active = False
                # user_input_buffer = "" #reset

        elif engine.key == 'LEFT':
            state = "LEFT"
        elif engine.key == 'RIGHT':
            state = "RIGHT"

        else:
            user_input_buffer.append(engine.key)
            user_input = ''.join(user_input_buffer)

def you_won():
    global current_state
    you_won = engine.load_image("Resources/background/istockphoto-1447471637-640x640.jpg")
    you_won.draw_fixed_size(0,0,engine.width,engine.height, False)
    engine.draw_text(f"Statistics  :",engine.width/2, 550)
    engine.draw_text(f"Incorrect typed words  :  {len(incorrect_words_count)}",engine.width/2, 600)



shoot_wait_counter = 0

def shoot():
    global shoot_wait_counter
    shoot_wait_counter += 1


    print(f"{shoot_wait_counter}")

    pass

def draw_shoot(x, y):
    list_shoot_img[0].draw_fixed_size(x, y, 25, 25)
    pass

    # usr_input = input("")

    # if usr_input == random_word:
    #     print("I got YOU!")

def in_game_time_counter():
    """
    :return:
    """
    global counter, wait_counter
    engine.color = 1,1,1
    engine.draw_text(f"TIME - {counter}", engine.width - 100, 50, True)

    wait_counter += 1
    if wait_counter > 10:
        counter += 1
        if counter > 2:
            wait_counter = 0

    return counter

def draw_heart():
    """
    Adds lives
    :return:
    """

    for i, heart in enumerate(list_char_heart):
        heart.draw_fixed_size(50 + i * 50 ,50,50,30)

    # list_char_heart[0].draw_fixed_size(50, 50, 50,30)
    # list_char_heart[1].draw_fixed_size(100, 50, 50,30)
    # list_char_heart[2].draw_fixed_size(150, 50, 50,30)

    pass

def you_died():
    print("You Lost")
    you_died = engine.load_image("Resources/background/b9b40e384d.jpg")
    you_died.draw_fixed_size(0, 0, engine.width,engine.height, False)
    engine.draw_text(f"Statistics  :", engine.width / 2, 550)
    engine.draw_text(f"Incorrect typed words  :  {len(incorrect_words_count)}", engine.width / 2, 600)

#Updated code
def check_dae_button():
    """
    Checks weather user clicks in the dae button boundries
    :return:
    """
    global current_state
    if engine.mouse_button == MouseButton.LEFT:
        if engine.colliding_pointinrect(engine.mouse_x, engine.mouse_y, engine.width - 100, 30, 100,40):
            return True
        cheat_mode()


def cheat_mode():
    """
    Enters cheat mode
    :return:
    """
    global current_state
    engine.background_color = 1,1,1
    engine.color = 0,0,0

    # for index,item in enumerate(words):
    #     print(f"{index}")
    distance = (50,100,150,200,250,300,350,400,450,500)
    for item,dist in zip(words,distance):
        engine.draw_text(f"{item}",engine.width/2, dist)


        # print(f"{item}",end="")


def render():
    """
    This function is being executed over and over, as fast as the frame rate. Use to draw (not update).
    """
    if current_state == Game.GAMEPLAY and difficulty_flag == True:
        in_game_time_counter()
        draw_background()
        draw_heart()
        draw_ground_plane()
        draw_rocks()
        draw_decorations()
        draw_grass()
        draw_character()
        display_random_word()
        draw_enemy()
        enemy_strike()
    if current_state == Game.WON:
        you_won()
    if current_state == Game.DEAD:
        you_died()

    if current_state == Game.CHEAT_MODE:
        cheat_mode()



    if state == "LEFT" and engine.key == "ENTER":
        draw_shoot(engine.width/2 -25, engine.height - engine.height/4 + 5)

    if state == "RIGHT" and engine.key == "ENTER":
        draw_shoot(engine.width/2 +75, engine.height - engine.height/4 +5)

    if current_state == Game.MENU:
        main_menu()


    if current_state == Game.LEVEL_SELECT:
        level_select()




    pass



def evaluate():
    """
    This function is being executed over and over, as fast as the frame rate. Use to update (not draw).
    """
    global shoot_wait_counter, current_state
    if current_state == Game.GAMEPLAY:
        walk_cycle_enemy(1)
        walk_cycle_enemy(2)
        walk_cycle_enemy(3)
        enemy_movement()
        enemy_strike()
        strike_enemy_counter()
        stop_enemy()
        shoot()
        if enemy_1 == 0 and enemy_2 == 0 and enemy_3 == 0:
            current_state = Game.WON

    if current_state == Game.WON:
        shoot_wait_counter +=1
        if shoot_wait_counter > 300:
            current_state = Game.MENU
            shoot_wait_counter = 0

    if current_state == Game.DEAD:
        shoot_wait_counter +=1
        if shoot_wait_counter > 300:
            current_state = Game.MENU
            shoot_wait_counter = 0

    if check_dae_button():
        current_state = Game.CHEAT_MODE

    #Updated code
    # if check_dae_button():
    #     current_state = Game.CHEAT_MODE
    #     print("Cheat")



    # if shoot_animation_active == "LEFT":
    #     shoot()

    pass


def mouse_pressed_event(mouse_x: int, mouse_y: int, mouse_button: MouseButton):
    """
    This function is only executed once each time a mouse button was pressed!
    """
    global current_state, difficulty, difficulty_flag
    if current_state == Game.MENU:
        if mouse_button == MouseButton.LEFT:
            if engine.colliding_pointinrect(engine.mouse_x, engine.mouse_y, engine.width / 2 - 100, engine.height - 100,
                                            200, 50):
                print("SUCCESS")
                current_state = Game.LEVEL_SELECT

    if current_state == Game.LEVEL_SELECT:
        if mouse_button == MouseButton.LEFT:
            if engine.colliding_pointinrect(engine.mouse_x, engine.mouse_y,engine.width/2 - 100,300,200,50):
                print("Easy")
                difficulty = "Easy"
                setup_random_words("Easy")
                difficulty_flag = True
                hearts()
                current_state = Game.GAMEPLAY


    if current_state == Game.LEVEL_SELECT:
        if mouse_button == MouseButton.LEFT:
            if engine.colliding_pointinrect(engine.mouse_x, engine.mouse_y,engine.width/2 - 100,400,200,50):
                print("Mid")
                difficulty = "Medium"
                setup_random_words("Medium")
                difficulty_flag = True
                hearts()
                current_state = Game.GAMEPLAY

    if current_state == Game.LEVEL_SELECT:
        if mouse_button == MouseButton.LEFT:
           if engine.colliding_pointinrect(engine.mouse_x, engine.mouse_y,engine.width/2 - 100,500,200,50):
                print("Hard")
                difficulty = "Hard"
                setup_random_words("Hard")
                difficulty_flag = True
                hearts()
                current_state = Game.GAMEPLAY
    pass


def key_up_event(key: str):
    """
    This function is only executed once each time a key was released!
    Special keys have more than 1 character, for example ESCAPE, BACKSPACE, ENTER, ...
    """
    if current_state == Game.GAMEPLAY:
        correct_random_word_trigger()

    pass


# Engine stuff; best not to mess with this:
engine._setup = setup
engine._evaluate = evaluate
engine._render = render
engine._mouse_pressed_event = mouse_pressed_event
engine._key_up_event = key_up_event

# Start the game loop:
engine.play()
