# -*- coding: Utf-8 -*

import pygame
from pygame.locals import *
from constantes import *

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

	def handleInput(self, game):
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				game.continuer = False

			elif event.type == KEYDOWN and event.key == K_F1:
				game.state = PlayingState()

	def update(self, game):
		pass

	def render(self, game):
		game.window.blit(self.background, (0,0))

class PlayingState(GameState):
	def __init__(self):
		self.cursor = Curseur(image_curseur)
		self.level = Niveau('Maps/n1')
		self.level.generer()

	def handleInput(self, game):
		for event in pygame.event.get():
			if event.type == QUIT:
				game.continuer = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				game.state = TitleScreenState()

	def update(self, game):
		pos = pygame.mouse.get_pos()
		self.cursor.AlignOnTopLeft(pos)

	def render(self, game):
		self.level.afficher(game.window)
		game.window.blit(self.cursor.image, (self.cursor.x, self.cursor.y))

class Map:
	def __init__(self, width, height):
		self.width = width
		self.height = height

class Niveau:
	"""Classe permettant de créer un niveau"""
	def __init__(self, fichier):
		self.fichier = fichier
		self.structure = 0


	def generer(self):
		"""Méthode permettant de générer le niveau en fonction du fichier.
		On crée une liste générale, contenant une liste par ligne à afficher"""
		#On ouvre le fichier
		with open(self.fichier, "r") as fichier:
			structure_niveau = []
			#On parcourt les lignes du fichier
			for ligne in fichier:
				ligne_niveau = []
				#On parcourt les sprites (lettres) contenus dans le fichier
				for sprite in ligne:
					#On ignore les "\n" de fin de ligne
					if sprite != '\n':
						#On ajoute le sprite à la liste de la ligne
						ligne_niveau.append(sprite)
				#On ajoute la ligne à la liste du niveau
				structure_niveau.append(ligne_niveau)
			#On sauvegarde cette structure
			self.structure = structure_niveau


	def afficher(self, fenetre):
		"""Méthode permettant d'afficher le niveau en fonction
		de la liste de structure renvoyée par generer()"""
		#Chargement des images (seule celle d'arrivée contient de la transparence)
		plaine = pygame.image.load(image_plaine).convert()
		foret = pygame.image.load(image_foret).convert()
		fort = pygame.image.load(image_fort).convert()

		#On parcourt la liste du niveau
		num_ligne = 0
		for ligne in self.structure:
			#On parcourt les listes de lignes
			num_case = 0
			for sprite in ligne:
				#On calcule la position réelle en pixels
				x = num_case * taille_sprite
				y = num_ligne * taille_sprite
				if sprite == 'p':
					fenetre.blit(plaine, (x,y))
				elif sprite == 'f':
				 	fenetre.blit(foret, (x,y))
				elif sprite == 'F':
					fenetre.blit(fort, (x,y))
				num_case += 1
			num_ligne += 1

class Curseur:
	"""Classe permettant de définir un curseur"""
	def __init__(self, image):
		self.image = pygame.image.load(image).convert_alpha()
		self.x = 0
		self.y = 0

	def AlignOnTopLeft(self, pos):
		self.x = int(pos[0] / sprite_width) * sprite_width
	 	self.y = int(pos[1] / sprite_height) * sprite_height