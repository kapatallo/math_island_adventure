import os
import pygame
import sys
import json
from MainPage import MainPage
from ArchipelagoPage import ArchipelagoPage

def main():

    # Définir le répertoire de travail au dossier contenant le script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    pygame.init()
    screen_width = 1000
    screen_height = 600
    screen = pygame.display.set_mode((1000, 600))

    # Charger les données du fichier JSON
    with open('question.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    # Fonction pour mettre à jour la progression du joueur
    def update_progression(level_index, question_index):
        data['islands'][level_index]['levels'][question_index]['completed'] = True

    # Fonction pour obtenir la progression d'une question
    def get_question_progression(level_index, question_index):
        return data['islands'][level_index]['levels'][question_index]['completed']

    # Extraire les titres des niveaux pour chaque île
    archipelago_data = {}
    for island in data['islands']:
        theme = island['theme'].lower()
        titles = [level['title'] for level in island['levels']]
        archipelago_data[theme] = {
            'titles': titles,
            'questions': island['levels']
        }

    # Définir les images du cours
    course_images = {
        "addition": ['cours/add1.png', 'cours/add2.png', 'cours/add3.png', 'cours/add4.png'],
        "soustraction": ['cours/sous1.png', 'cours/sous2.png', 'cours/sous3.png', 'cours/sous4.png'],
        "multiplication": ['cours/mul1.png', 'cours/mul2.png', 'cours/mul3.png', 'cours/mul4.png', 'cours/mul5.png'],
        "division": ['cours/div1.png', 'cours/div2.png', 'cours/div3.png', 'cours/div4.png']
    }

    main_page = MainPage(screen, screen_width, screen_height)

    def return_to_main_page():
        nonlocal current_page
        main_page.current_archipelago = None  # Reset the current archipelago to None
        current_page = main_page

    archipelago_pages = {
        "addition": ArchipelagoPage(screen, 'arch_add.png', 'avatar.png', 'avatar_moving.png', 'ilot_done.png', 'ilot_locked.png', 
                                    [(150, 150), (750, 160), (190, 470), (700, 460), (100, 300), (800, 320)], 'back.png', archipelago_data['addition']['titles'], archipelago_data['addition']['questions'], course_images['addition'], return_to_main_page,'Addition'),
        "soustraction": ArchipelagoPage(screen, 'arch_sous.png', 'avatar.png', 'avatar_moving.png', 'ilot_done.png', 'ilot_locked.png', 
                                    [(150, 150), (750, 160), (190, 470), (700, 460), (100, 300), (800, 320)], 'back.png', archipelago_data['soustraction']['titles'], archipelago_data['soustraction']['questions'], course_images['soustraction'], return_to_main_page,'Soustraction'),
        "multiplication": ArchipelagoPage(screen, 'arch_mul.png', 'avatar.png', 'avatar_moving.png', 'ilot_done.png', 'ilot_locked.png', 
                                    [(150, 150), (750, 160), (190, 470), (700, 460), (100, 300), (800, 320)], 'back.png', archipelago_data['multiplication']['titles'], archipelago_data['multiplication']['questions'], course_images['multiplication'], return_to_main_page,'Multiplication'),
        "division": ArchipelagoPage(screen, 'arch_div.png', 'avatar.png', 'avatar_moving.png', 'ilot_done.png', 'ilot_locked.png', 
                                    [(150, 150), (750, 160), (190, 470), (700, 460), (100, 300), (800, 320)], 'back.png', archipelago_data['division']['titles'], archipelago_data['division']['questions'], course_images['division'], return_to_main_page,'Division'),
    }

    current_page = main_page
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            current_page.handle_event(event)

        if main_page.current_archipelago:
            current_page = archipelago_pages[main_page.current_archipelago]

        current_page.update()

if __name__ == "__main__":
    main()
