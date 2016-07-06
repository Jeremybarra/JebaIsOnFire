# -*- coding: Utf-8 -*

import pygame
from pygame.locals import *
from constantes import *

class Map:
	def __init__(self, width, height):
		self.width = width
		self.height = height

class Niveau:
	"""Classe permettant de créer un niveau"""
	def __init__(self, fichier):
		self.fichier = fichier
		self.structure = 0
		self.width = 0
		self.height = 0

	def generer(self):
		"""Méthode permettant de générer le niveau en fonction du fichier.
		On crée une liste générale, contenant une liste par ligne à afficher"""
		#On ouvre le fichier
		with open(self.fichier, "r") as fichier:
			structure_niveau = []
			#On parcourt les lignes du fichier
			for ligne in fichier:
				self.height += 1
				self.width = len(ligne)
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
				x = num_case * sprite_width
				y = num_ligne * sprite_height
				if sprite == 'p':
					fenetre.blit(plaine, (x,y))
				elif sprite == 'f':
				 	fenetre.blit(foret, (x,y))
				elif sprite == 'F':
					fenetre.blit(fort, (x,y))
				num_case += 1
			num_ligne += 1
