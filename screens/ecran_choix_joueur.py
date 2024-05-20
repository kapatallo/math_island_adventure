import pygame

def ecran_choix_joueur(ecran):
    bouton_j1 = pygame.Rect(100, 200, 200, 50)
    bouton_j2 = pygame.Rect(340, 200, 200, 50)

    while True:
        ecran.fill((0, 0, 0))  # Nettoyer l'écran
        pygame.draw.rect(ecran, (255, 0, 0), bouton_j1)
        pygame.draw.rect(ecran, (0, 0, 255), bouton_j2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_j1.collidepoint(event.pos):
                    return "Joueur 1"
                elif bouton_j2.collidepoint(event.pos):
                    return "Joueur 2"

        pygame.display.flip()
