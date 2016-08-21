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
		self.img_mouvement_possibles = pygame.image.load(image_mouvements_possibles).convert_alpha()

	def displayPossibleMovement(self, niveau):
		for x in range(0, niveau.width):
			for y in range(0, niveau.height):
				if distanceCases((x, y), (self.case_x, self.case_y)) <= self.deplacement:
					self.mouvement_possibles[(x, y)] = True

	def maskPossibleMovement(self):
		for key in self.mouvement_possibles:
			self.mouvement_possibles[key] = False

	def move(self, direction):
		"""Methode permettant de déplacer le personnage"""

		#Déplacement vers la droite
		if direction == 'right':
			#Pour ne pas dépasser l'écran
			if self.case_x < (nombre_sprite_cote - 1):
				#On vérifie que la case de destination n'est pas un mur
				if self.niveau.structure[self.case_y][self.case_x+1] != 'm':
					#Déplacement d'une case
					self.case_x += 1
					#Calcul de la position "réelle" en pixel
					self.x = self.case_x * taille_sprite
			#Image dans la bonne direction
			self.direction = self.right

		#Déplacement vers la gauche
		if direction == 'left':
			if self.case_x > 0:
				if self.niveau.structure[self.case_y][self.case_x-1] != 'm':
					self.case_x -= 1
					self.x = self.case_x * taille_sprite
			self.direction = self.left


		#Déplacement vers le bas
		if direction == 'backward':
			if self.case_y < (nombre_ligne - 1):
				if self.niveau.structure[self.case_y+1][self.case_x] != 'm':
					self.case_y += 1
					self.y = self.case_y * taille_sprite
			self.direction = self.backward

		#Déplacement vers le haut
		if direction == 'forward':
			if self.case_y > 0:
				if self.niveau.structure[self.case_y-1][self.case_x] != 'm':
					self.case_y -= 1
					self.y = self.case_y * taille_sprite
			self.direction = self.forward

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

		if owner >= 0 and owner < player_number:
			self.owner = owner
		else:
			self.owner = 0
		self.mouvement_possibles = {}
		self.img_mouvement_possibles = pygame.image.load(image_mouvements_possibles).convert_alpha()
