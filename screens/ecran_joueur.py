import pygame
import sys

def ecran_joueur1(ecran):
    # Logique de l'écran pour le Joueur 1
    ecran.fill((255, 255, 255))  # Fond blanc
    pygame.display.flip()
    pygame.time.wait(3000)  # Attendre 3 secondes

def ecran_joueur2(ecran):
    # Logique de l'écran pour le Joueur 2
    ecran_joueur1