# -*- coding: Utf-8 -*

import pygame
from pygame.locals import *
from constantes import *
from classes import *
from personnages import *
from buttons import *

class Game:
	def __init__(self, map_width, map_height):
		self.map = Map(map_width, map_height)
		# Initialisation (pygame, fenetre etc..)
		self.window = pygame.display.set_mode((map_width * sprite_width, map_height * sprite_height), RESIZABLE)
		icone = pygame.image.load(image_icone)
		pygame.display.set_icon(icone)
		pygame.display.set_caption(titre_fenetre)

		self.state = TitleScreenState()
		self.clearColor = pygame.Surface(self.window.get_size())
		color = 255, 255, 255
		self.clearColor.fill(color)

	def run(self):
		self.continuer = True
		while(self.continuer):
			pygame.time.Clock().tick(30)

			self.state.handleInput(self)
			self.state.update(self)

			self.clearWindow()
			self.state.render(self)
			pygame.display.flip()

	def clearWindow(self):
		self.window.blit(self.clearColor, (0,0))

class GameState:
	def handleInput(self, game):
		pass
	def update(self, game):
		pass
	def render(self, game):
		pass

class TitleScreenState(GameState):
	def __init__(self):
		self.background = pygame.image.load(image_accueil).convert()
		self.font = pygame.font.SysFont('Arial', 25)

		self.start_button = StartButton()
		self.quit_button = QuitButton()

	def handleInput(self, game):
		for event in pygame.event.get():
			mouse = pygame.mouse.get_pos()
			if event.type == QUIT:
				game.continuer = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					self.from_menu_to_somewhere(mouse, game)
			self.start_button.manage_mouse_pos(mouse, game, self.background, event)
			self.quit_button.manage_mouse_pos(mouse, game, self.background, event)

	def update(self, game):
		pass

	def render(self, game):
		game.window.blit(self.background, (0,0))

	def from_menu_to_somewhere(self, mouse, game):
		if self.start_button.mouse_on_start_button(mouse):
			game.state = PlayingState()
		elif self.quit_button.mouse_on_leave_button(mouse):
			game.continuer = False

class PlayingState(GameState):
	def __init__(self):
		self.cursor = Curseur(image_curseur)
		self.level = Niveau('Maps/n1')
		self.level.generer()
		self.currentPlayer = 0
		self.units = {}
		self.units[(1, 1)] = Myrmidon(1, 1, image_myrmidon, image_myrmidon, image_myrmidon, image_myrmidon, None, 5, 0)
		self.units[(8, 8)] = Myrmidon(8, 8, image_myrmidon, image_myrmidon, image_myrmidon, image_myrmidon, None, 5, 0)
		self.units[(12, 12)] = Myrmidon(12, 12, image_myrmidon, image_myrmidon, image_myrmidon, image_myrmidon, None, 5, 1)

	def handleInput(self, game):
		for event in pygame.event.get():
			if event.type == QUIT:
				game.continuer = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				game.state = TitleScreenState()
			elif event.type == KEYDOWN and event.key == K_e:
				self.end_turn()
			elif event.type == MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				case_pos = (pos[0] / sprite_width, pos[1] / sprite_height)
				self.manage_onclick(event, case_pos)

	def end_turn(self):
		self.currentPlayer = (self.currentPlayer + 1) % player_number
		self.mask_all_possible_movements()
		self.set_all_units_undone()

	def set_all_units_undone(self):
		for unit in self.units.values():
			unit.is_done = False

	def mask_all_possible_movements(self):
		for key in self.units:
			self.units[key].maskPossibleMovement()

	def manage_onclick(self, event, case_pos):
		if event.button == 1: #Left Click
			self.manage_left_click(case_pos)
		elif event.button == 3: #Right Click
			self.manage_right_click(case_pos)

	def manage_left_click(self, case_pos):
		if case_pos in self.units:
			self.onclick_unit(case_pos)

	def manage_right_click(self, case_pos):
		possible_cases = False
		for position, unit in self.units.items():
			if unit.movement_displayed:
				possible_cases = unit.mouvement_possibles
				if case_pos in possible_cases:
					self.units[case_pos] = self.units.pop(position) #Update de la position de l'unité
					unit.move(case_pos)                             

	def onclick_unit(self, case_pos):
		if self.units[case_pos].owner == self.currentPlayer and not self.units[case_pos].is_done:
			if self.units[case_pos].movement_displayed:			#Click sur une unité déjà sélectionnée
				self.units[case_pos].maskPossibleMovement()		#On masque ses mouvements possibles
			else:
				for case in self.units.keys():
					if case != case_pos:
						self.units[case].maskPossibleMovement()
				self.units[case_pos].displayPossibleMovement(self.level)

	def update(self, game):
		pos = pygame.mouse.get_pos()
		self.cursor.AlignOnTopLeft(pos)

	def render(self, game):
		self.level.display(game.window)
		for key in self.units:
			self.units[key].display(game.window)
		game.window.blit(self.cursor.image, (self.cursor.x, self.cursor.y))

class Curseur:
	"""Classe permettant de définir un curseur"""
	def __init__(self, image):
		self.image = pygame.image.load(image).convert_alpha()
		self.x = 0
		self.y = 0

	def AlignOnTopLeft(self, pos):
		self.x = int(pos[0] / sprite_width) * sprite_width
	 	self.y = int(pos[1] / sprite_height) * sprite_height
