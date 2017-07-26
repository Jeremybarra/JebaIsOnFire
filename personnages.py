# -*- coding: Utf-8 -*
"""Classes du jeu Fire Emblem"""

import pygame
from pygame.locals import *
from constantes import *
from math import *

def distanceCases(case1, case2):
	return sqrt((case2[0] - case1[0])**2 + (case2[1] - case1[1])**2)

class Character:
	"""Classe permettant de créer un personnage"""
	def __init__(self, pos_x, pos_y, right, left, forward, backward, niveau, deplacement, owner):
		#Sprites du personnage
		self.right = pygame.image.load(right).convert_alpha()
		self.left = pygame.image.load(left).convert_alpha()
		self.forward = pygame.image.load(forward).convert_alpha()
		self.backward = pygame.image.load(backward).convert_alpha()
		#Position du personnage en cases et en pixels
		self.case_x = pos_x
		self.case_y = pos_x
		#Direction par défaut
		self.direction = self.right
		#Niveau dans lequel le personnage se trouve
		self.niveau = niveau
		self.deplacement = deplacement

		if owner >= 0 and owner < player_number:
			self.owner = owner
		else:
			self.owner = 0
		self.mouvement_possibles = {}
		self.movement_displayed = False
		self.is_done = False
		self.img_mouvement_possibles = pygame.image.load(image_mouvements_possibles).convert_alpha()

	def displayPossibleMovement(self, niveau):
		for x in range(0, niveau.width):
			for y in range(0, niveau.height):
				if distanceCases((x, y), (self.case_x, self.case_y)) <= self.deplacement:
					self.mouvement_possibles[(x, y)] = True
		self.movement_displayed = True

	def maskPossibleMovement(self):
		for key in self.mouvement_possibles:
			self.mouvement_possibles[key] = False
		self.movement_displayed = False

	def move(self, position):
		self.case_x = position[0]
		self.case_y = position[1]
		self.maskPossibleMovement()
		self.is_done = True

	def display(self, fenetre):
		for key in self.mouvement_possibles:
			if self.mouvement_possibles[key]:
				fenetre.blit(self.img_mouvement_possibles, (key[0] * sprite_width, key[1] * sprite_height))
		fenetre.blit(self.direction, (self.case_x * sprite_width, self.case_y * sprite_height))

class Myrmidon(Character):
	"""Classe permettant de créer un myrmidon"""
	def __init__(self, pos_x, pos_y, right, left, forward, backward, niveau, owner):
		#Sprites du personnage
		self.right = pygame.image.load(right).convert_alpha()
		self.left = pygame.image.load(left).convert_alpha()
		self.forward = pygame.image.load(forward).convert_alpha()
		self.backward = pygame.image.load(backward).convert_alpha()
		#Position du personnage en cases et en pixels
		self.case_x = pos_x
		self.case_y = pos_x
		#Direction par défaut
		self.direction = self.right
		#Niveau dans lequel le personnage se trouve
		self.niveau = niveau
		self.deplacement = 5.0
		self.movement_displayed = False

		if owner >= 0 and owner < player_number:
			self.owner = owner
		else:
			self.owner = 0
		self.mouvement_possibles = {}
		self.is_done = False
		self.img_mouvement_possibles = pygame.image.load(image_mouvements_possibles).convert_alpha()
