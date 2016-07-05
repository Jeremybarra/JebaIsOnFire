# -*- coding: Utf-8 -*
import pygame
from pygame.locals import *

from classes import *
from constantes import *

pygame.init()

#Ouverture de la fenêtre Pygame 
fenetre = pygame.display.set_mode((longueur_fenetre, hauteur_fenetre), RESIZABLE)
#Icone
icone = pygame.image.load(image_icone)
pygame.display.set_icon(icone)
#Titre
pygame.display.set_caption(titre_fenetre)


#BOUCLE PRINCIPALE
continuer = 1
while continuer:	
	#Chargement et affichage de l'écran d'accueil
	accueil = pygame.image.load(image_accueil).convert()
	fenetre.blit(accueil, (0,0))

	#Rafraichissement
	pygame.display.flip()

	#On remet ces variables à 1 à chaque tour de boucle
	continuer_jeu = 1
	continuer_accueil = 1

	#BOUCLE D'ACCUEIL
	while continuer_accueil:
	
		#Limitation de vitesse de la boucle
		pygame.time.Clock().tick(30)
	
		for event in pygame.event.get():
		
			#Si l'utilisateur quitte, on met les variables 
			#de boucle à 0 pour n'en parcourir aucune et fermer
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				continuer_accueil = 0
				continuer_jeu = 0
				continuer = 0
				#Variable de choix du niveau
				choix = 0
				
			elif event.type == KEYDOWN:				
				#Lancement du niveau 1
				if event.key == K_F1:
					continuer_accueil = 0	#On quitte l'accueil
					choix = 'Maps/n1'		#On définit le niveau à charger
				#Lancement du niveau 2
				elif event.key == K_F2:
					continuer_accueil = 0
					choix = 'Maps/n2'
			
		

	#on vérifie que le joueur a bien fait un choix de niveau
	#pour ne pas charger s'il quitte
	if choix != 0:
		#Chargement du fond
		fond = pygame.image.load(image_fond).convert()

		#Génération d'un niveau à partir d'un fichier
		niveau = Niveau(choix)
		niveau.generer()
		niveau.afficher(fenetre)

		#Création du perso
		myrmidon = Myrmidon(500, 500, image_myrmidon, image_myrmidon, image_myrmidon, image_myrmidon, niveau)
		myrmidon_femme = Myrmidon(400, 400, image_myrmidon, image_myrmidon, image_myrmidon, image_myrmidon, niveau)
		curseur = Curseur(image_curseur, niveau)
				
	#BOUCLE DE JEU
	while continuer_jeu:
	
		#Limitation de vitesse de la boucle
		pygame.time.Clock().tick(30)
		pos = pygame.mouse.get_pos()
		curseur.x = int(pos[0] / taille_sprite) * taille_sprite
		curseur.y = int(pos[1] / taille_sprite) * taille_sprite

		mousepress = pygame.mouse.get_pressed()

	
		for event in pygame.event.get():
		
			#Si l'utilisateur quitte, on met la variable qui continue le jeu
			#ET la variable générale à 0 pour fermer la fenêtre
			if event.type == QUIT:
				continuer_jeu = 0
				continuer = 0
		
			elif event.type == KEYDOWN:
				#Si l'utilisateur presse Echap ici, on revient seulement au menu
				if event.key == K_ESCAPE:
					continuer_jeu = 0

				#Touches de déplacement du curseur
				# elif event.key == K_RIGHT:
				# 	curseur.deplacer('droite')
				# elif event.key == K_LEFT:
				# 	curseur.deplacer('gauche')
				# elif event.key == K_UP:
				# 	curseur.deplacer('haut')
				# elif event.key == K_DOWN:
				# 	curseur.deplacer('bas')

		#Affichages aux nouvelles positions
		fenetre.blit(fond, (0,0))
		niveau.afficher(fenetre)
		fenetre.blit(curseur.direction, (curseur.x, curseur.y))
		fenetre.blit(myrmidon.direction, (myrmidon.x, myrmidon.y)) 
		fenetre.blit(myrmidon_femme.direction, (myrmidon_femme.x, myrmidon_femme.y))
		pygame.display.flip()

