import sys
import os
from tkinter import *
import PIL
from PIL import Image
import random
import numpy as np
import pygame
from pygame.locals import *

# Initialize some values. Some may not be used...whoops.
TKroot = Tk()
h,w = 1000,1000
border = 15
N = 0
gray_background = (28, 28, 28)
lighter_gray_background = (34, 34, 34)
light_yellow = (235, 255, 218)

# Dumb. But necessary.
button_down = False




# Set the path for the main directory and the blank board.
dir = os.path.dirname(os.path.abspath(__file__))
FILE_LOCATION_MAIN_POSTER = os.path.join(dir, "CPAllPictures\Compliment Poster Blank.png")

# Set the options for adjectives and nouns and creates dictionaries with their pixel positions for use later.
file_names_adj = ["Chaotic", "Fancy", "Fierce", "Majestic", "Powerful", "Stunning", "Unique", "Wholesome"]
file_names_adj_placement = {
    "Chaotic" : [500, 184],
    "Fancy" : [633, 523],
    "Fierce" : [477, 297],
    "Majestic" : [50, 184],
    "Powerful" : [437, 410],
    "Stunning" : [50, 297],
    "Unique" : [50, 410],
    "Wholesome" : [35, 523]
}
file_names_noun = ["Cat", "Eagle", "Flower", "Human", "Lion", "Mountain", "Potato", "Tree"]
file_names_noun_placement = {
    "Cat" : [400, 636],
    "Eagle" : [633, 636],
    "Flower" : [334, 749],
    "Human" : [50, 636],
    "Lion" : [690, 749],
    "Mountain" : [38, 862],
    "Potato" : [535, 862],
    "Tree" : [50, 749]
}

# Makes the random selection of adjective and noun and prepares and returns the proper file paths.
def select_stuff():

    # Generate the random choice for adjective and noun and fix the choice to include my weird naming of the files.
    file_get_adj = random.choice(file_names_adj)
    adj_coordinates = file_names_adj_placement.get(file_get_adj)
    file_get_adj = "CP"+file_get_adj
    file_get_noun = random.choice(file_names_noun)
    noun_coordinates = file_names_noun_placement.get(file_get_noun)
    file_get_noun = "CP"+file_get_noun

    FILE_LOCATION_FIRST = os.path.join(dir, "CPAllPictures\{}.png".format(file_get_adj))
    FILE_LOCATION_SECOND = os.path.join(dir, "CPAllPictures\{}.png".format(file_get_noun))

    return FILE_LOCATION_FIRST, FILE_LOCATION_SECOND, adj_coordinates, noun_coordinates

# Makes the composite image using the file paths from the select_stuff function. Images are overlayed on top of each other using PIL and the coordinate information from the dictionaries above.
def make_image():

    adj_file_location, noun_file_location, adjective_coord, noun_coord = select_stuff()
    img = Image.open(FILE_LOCATION_MAIN_POSTER)
    img2 = Image.open(adj_file_location)
    img3 = Image.open(noun_file_location)
    img.paste(img2, (adjective_coord[0], adjective_coord[1]), img2)
    img.paste(img3, (noun_coord[0], noun_coord[1]), img3)
    #img.show()

    return img

# Defines our text objects.
def text_objects(text, font):
    textSurface = font.render(text, True, light_yellow)
    return textSurface, textSurface.get_rect()

# Converts the PIL image to a pygame image and updates the screen with the new image.
def change_image(screen, windoww_init, windowh_init, current_size):

    image2print = make_image()

    mode = image2print.mode
    size = image2print.size
    data = image2print.tobytes()

    this_image = pygame.image.fromstring(data, size, mode)
    screen.blit(this_image, (border, border))

    currentw, currenth = pygame.display.get_surface().get_size()
    if currentw != windoww_init or currenth != windowh_init:
        screen.blit(pygame.transform.scale(this_image, (currentw, currenth)), (0, 0))
    
    pygame.display.flip()
        
# Checks for a click on the button and triggers the change_image function when clicked.
def button(currentw, currenth, screen, windoww_init, windowh_init, current_size):
    global button_down
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect_x = currentw*(1/3)
    rect_y = currenth*(95/100)
    rect_len = currentw/3
    rect_hight = currenth/20

    if rect_x + rect_len > mouse[0] > rect_x and rect_y + rect_hight > mouse[1] > rect_y:
        pygame.draw.rect(screen, lighter_gray_background, (rect_x, rect_y, rect_len, rect_hight))
        if click[0] == 1 and not button_down:
            
            change_image(screen, windoww_init, windowh_init, current_size)
            button_down = True
            
        elif click[0] == 0:
            button_down = False
    else:
        pygame.draw.rect(screen, gray_background, (rect_x, rect_y, rect_len, rect_hight))
    
    font_sizeh = currenth/21
    font_sizew = currentw/3
    font_size = (font_sizeh + font_sizew) /10 
    font_size = round(font_size)
    text_font = pygame.font.Font("AllertaStencil-Regular.ttf", font_size)
    textSurf, textRect = text_objects("Compliment Me!", text_font)
    textRect.center = ( (rect_x+(rect_len/2)), (rect_y+(rect_hight/2)) )
    screen.blit(textSurf, textRect)

# Puts it all together.
def main():

    # Initializing pygame and setting default values.
    pygame.init()
    screen = pygame.display.set_mode((w+(2*border), h+(2*border)), HWSURFACE | DOUBLEBUF | RESIZABLE)
    pygame.display.set_caption("Have A Compliment!")
    done = False
    clock = pygame.time.Clock()
    windoww_init, windowh_init = pygame.display.get_surface().get_size()
    start = 0

    screen.fill((0,0,0))

    # Loop for the "game".
    while True:

        # Check events and allow user to exit.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Records the current size from the initial size.
        current_size = (windoww_init, windowh_init)
        
        # If the program has just been opened, generate one random photo for the initial screen.
        if start == 0:
            
            image = make_image()

            mode = image.mode
            size = image.size
            data = image.tobytes()

            this_image = pygame.image.fromstring(data, size, mode)
            screen.blit(this_image, (border, border))
            
            start += 1
            pygame.display.flip()

        # Check to see if the user has resized the page and adjust the current screen to match.
        if event.type == pygame.VIDEORESIZE:
            if event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(
                    event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                screen.blit(pygame.transform.scale(this_image, event.dict['size']), (0, 0))
                current_size = event.dict['size']
                pygame.display.flip()
        
        # Update current size values in case they changed.
        currentw, currenth = pygame.display.get_surface().get_size()

        # Call the button function to do the thing.
        button(currentw, currenth, screen, windoww_init, windowh_init, current_size)
        
        # Update the display.
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()