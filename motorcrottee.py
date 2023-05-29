## main game script

# import some packages
from Pygame_Functions.pygame_functions import *
import pygame
import os
import player as controls
import collectibles
import traffic as obstacles
import sidewalk
from sound_elements import *
import game_configuration as settings
import enemies

setAutoUpdate(False)

def sort_sprites_by_ground_position(spriteGroup, vehicle_list, sidewalk_element_list, poop_list, enemy_list, bullets, hero):
    # Sort the sprites based on their bottom Y position
    my_private_sprite_group = vehicle_list + sidewalk_element_list + poop_list + enemy_list + bullets
    my_private_sprite_group.append(hero)  
    layer_order = sorted(my_private_sprite_group, key=lambda sprite: sprite.ground_position)
    
    # Add the sprites back to the sprite group in the correct order
    for i, sprite in enumerate(layer_order):
        try:
            spriteGroup.change_layer(sprite.sprite, i)
        except:
            pass

def draw_text(surface, text, size, x, y):
    # choose a font (you can choose another if you like)
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, 'WHITE')  # True stands for anti-aliasing, WHITE is the color of the text which is usually defined as (255, 255, 255)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def show_start_screen():
    # Load the image
    background = pygame.image.load("media/images/main1.png")  # Replace 'background_image_path.png' with the path to your image file
    background = pygame.transform.scale(background, (settings.screen_size_x, settings.screen_size_y))  # Scale the image to fit the screen

    # Draw the image
    screen.blit(background, (0, 0))

    # Draw the text
    draw_text(screen, "MOTOCROTTE", 64, settings.screen_size_x / 2, settings.screen_size_y / 4)
    draw_text(screen, "Press any key to start", 18, settings.screen_size_x / 2, settings.screen_size_y / 2)

    # Update the display
    pygame.display.flip()

    # Start screen Music Loop Begins:
    pygame.mixer.music.load('media/mainRiff.wav')
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(loops=-1)

    # Wait for the player to press a key
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# set screen
screen = screenSize(settings.screen_size_x, settings.screen_size_y)

# Show the start screen
show_start_screen()

# set scrolling background
bg = setBackgroundImage( [  ["media/images/new_background5.png", "media/images/new_background5.png"]  ])


#init frames
frame=0
nextFrame = clock()


# Game Music Loop Begins:
#pygame.mixer.music.load('media/sounds/Action-Rock.mp3')
#pygame.mixer.music.set_volume(0.4)
#pygame.mixer.music.play(loops=-1)


# init player
hero = controls.Player()
bullets = controls.bullets

# set up empty lists for game elements
vehicle_list = []
poop_list = []
sidewalk_element_list = []
enemy_list = []

#main game loop
while True:
    
    scrollBackground((int(hero.x_velocity)*-1),0)   # scroll the background by negative ratio to the player's speed
    
    hero.move()   # update the player's actions
    
    obstacles.update_display(vehicle_list, hero, bullets, enemy_list) # update the traffic
    
    sidewalk.update_display(sidewalk_element_list, hero, bullets) # update the sidewalk
    
    collectibles.update_display(poop_list, hero)  # update the poop
    
    enemies.update_display(enemy_list, hero, bullets)
    
    # sort the spriteGroup based on the y position of the bottom of each sprite
    sort_sprites_by_ground_position(spriteGroup, vehicle_list, sidewalk_element_list, poop_list, enemy_list, bullets, hero)
        
    updateDisplay()
    tick(120)

endWait()