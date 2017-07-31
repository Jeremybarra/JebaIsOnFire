import pygame
from pygame.locals import *
from constantes import *

class Button:
    def __init__(self):
        self.font = pygame.font.SysFont('Arial', 25)

class StartButton(Button):
    def __init__(self):
        Button.__init__(self)

    def manage_mouse_pos(self, mouse, game, background, event):
        self.manage_start_button_colors(mouse, background)
        self.manage_start_button_texts(background)

    def manage_start_button_colors(self, mouse, background):
    	if self.mouse_on_start_button(mouse):
    		pygame.draw.rect(background, start_game_button_color_highlight, start_game_button_features)
    	else:
    		pygame.draw.rect(background, start_game_button_color, start_game_button_features)

    def manage_start_button_texts(self, background):
    	launch_game_text = self.font.render('Lancer', True, black_color)
    	launch_game_text_rect = launch_game_text.get_rect()
    	launch_game_text_rect.center = (start_game_button_x + (start_game_button_witdh / 2),start_game_button_y + (start_game_button_height / 2))
    	background.blit(launch_game_text, launch_game_text_rect)

    def mouse_on_start_button(self, mouse):
    	if start_game_button_x + start_game_button_witdh > mouse[0] > start_game_button_x and start_game_button_y + start_game_button_height > mouse[1] > start_game_button_y:
    		return True
    	return False

class QuitButton(Button):
    def __init__(self):
        Button.__init__(self)

    def manage_mouse_pos(self, mouse, game, background, event):
        self.manage_quit_button_colors(mouse, background)
        self.manage_quit_button_texts(background)

    def manage_quit_button_colors(self, mouse, background):
        if self.mouse_on_leave_button(mouse):
            pygame.draw.rect(background, leave_game_button_color_highlight, leave_game_button_features)
        else:
            pygame.draw.rect(background, leave_game_button_color, leave_game_button_features)

    def manage_quit_button_texts(self, background):
    	leave_game_text = self.font.render('Quitter', True, black_color)
    	leave_game_text_rect = leave_game_text.get_rect()
    	leave_game_text_rect.center = (leave_game_button_x + (leave_game_button_witdh / 2), leave_game_button_y + (leave_game_button_height / 2))
    	background.blit(leave_game_text, leave_game_text_rect)

    def mouse_on_leave_button(self, mouse):
    	if leave_game_button_x + leave_game_button_witdh > mouse[0] > leave_game_button_x and leave_game_button_y + leave_game_button_height > mouse[1] > leave_game_button_y:
    		return True
    	return False
