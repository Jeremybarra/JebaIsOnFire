# -*- coding: Utf-8 -*
"""Classes du jeu Fire Emblem"""

import pygame
from pygame.locals import *
from constantes import *

class Personnage:
	"""Classe permettant de créer un personnage"""
	def __init__(self, pos_x, pos_y, droite, gauche, haut, bas, niveau, deplacement, proprietaire):
		#Sprites du personnage
		self.droite = pygame.image.load(droite).convert_alpha()
		self.gauche = pygame.image.load(gauche).convert_alpha()
		self.haut = pygame.image.load(haut).convert_alpha()
		self.bas = pygame.image.load(bas).convert_alpha()
		#Position du personnage en cases et en pixels
		self.case_x = pos_x
		self.case_y = pos_x
		#Direction par défaut
		self.direction = self.droite
		#Niveau dans lequel le personnage se trouve
		self.niveau = niveau
		self.deplacement = deplacement

		if proprietaire >= 0 and proprietaire < player_number:
			self.proprietaire = proprietaire
		else:
			self.proprietaire = 0

	def deplacer(self, direction):
		"""Methode permettant de déplacer le personnage"""

		#Déplacement vers la droite
		if direction == 'droite':
			#Pour ne pas dépasser l'écran
			if self.case_x < (nombre_sprite_cote - 1):
				#On vérifie que la case de destination n'est pas un mur
				if self.niveau.structure[self.case_y][self.case_x+1] != 'm':
					#Déplacement d'une case
					self.case_x += 1
					#Calcul de la position "réelle" en pixel
					self.x = self.case_x * taille_sprite
			#Image dans la bonne direction
			self.direction = self.droite

		#Déplacement vers la gauche
		if direction == 'gauche':
			if self.case_x > 0:
				if self.niveau.structure[self.case_y][self.case_x-1] != 'm':
					self.case_x -= 1
					self.x = self.case_x * taille_sprite
			self.direction = self.gauche


		#Déplacement vers le bas
		if direction == 'bas':
			if self.case_y < (nombre_ligne - 1):
				if self.niveau.structure[self.case_y+1][self.case_x] != 'm':
					self.case_y += 1
					self.y = self.case_y * taille_sprite
			self.direction = self.bas

		#Déplacement vers le haut
		if direction == 'haut':
			if self.case_y > 0:
				if self.niveau.structure[self.case_y-1][self.case_x] != 'm':
					self.case_y -= 1
					self.y = self.case_y * taille_sprite
			self.direction = self.haut

	def afficher(self, fenetre):
		fenetre.blit(self.direction, (self.case_x * sprite_width, self.case_y * sprite_height))

class Myrmidon(Personnage):
	"""Classe permettant de créer un myrmidon"""
	def __init__(self, pos_x, pos_y, droite, gauche, haut, bas, niveau):
		#Sprites du personnage
		self.droite = pygame.image.load(droite).convert_alpha()
		self.gauche = pygame.image.load(gauche).convert_alpha()
		self.haut = pygame.image.load(haut).convert_alpha()
		self.bas = pygame.image.load(bas).convert_alpha()
		#Position du personnage en cases et en pixels
		self.case_x = pos_x
		self.case_y = pos_y
		#Direction par défaut
		self.direction = self.droite
		#Niveau dans lequel le personnage se trouve
		self.niveau = niveau
		self.deplacement = 5
