# -*- coding: Utf-8 -*
"""Classes du jeu Fire Emblem"""

import pygame
from pygame.locals import *
from constantes import *

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
			pygame.time.Clock().tick(60)

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

class Personnage:
	"""Classe permettant de créer un myrmidon"""
	def __init__(self, pos_x, pos_y, droite, gauche, haut, bas, niveau, deplacement):
		#Sprites du personnage
		self.droite = pygame.image.load(droite).convert_alpha()
		self.gauche = pygame.image.load(gauche).convert_alpha()
		self.haut = pygame.image.load(haut).convert_alpha()
		self.bas = pygame.image.load(bas).convert_alpha()
		#Position du personnage en cases et en pixels
		self.case_x = 0
		self.case_y = 0
		self.x = pos_x
		self.y = pos_y
		#Direction par défaut
		self.direction = self.droite
		#Niveau dans lequel le personnage se trouve
		self.niveau = niveau
		self.deplacement = deplacement


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

class Myrmidon(Personnage):
	"""Classe permettant de créer un myrmidon"""
	def __init__(self, pos_x, pos_y, droite, gauche, haut, bas, niveau):
		#Sprites du personnage
		self.droite = pygame.image.load(droite).convert_alpha()
		self.gauche = pygame.image.load(gauche).convert_alpha()
		self.haut = pygame.image.load(haut).convert_alpha()
		self.bas = pygame.image.load(bas).convert_alpha()
		#Position du personnage en cases et en pixels
		self.case_x = 0
		self.case_y = 0
		self.x = pos_x
		self.y = pos_y
		#Direction par défaut
		self.direction = self.droite
		#Niveau dans lequel le personnage se trouve
		self.niveau = niveau
		self.deplacement = 5


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
