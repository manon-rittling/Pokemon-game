import pygame
from pygame.locals import *
import sys
from classes.Ajouter_pokemon import *
from classes.Pokedex import *
from classes.Nouvelle_partie import *


def lancer_jeu():
    pygame.init()

    
    menu = Menu_principal()
    ajouter = Ajouter_pokemon()
    acces_pokedex = None
    combat = Nouvelle_partie(800,800)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if menu.lancer_jeu_rect.collidepoint(event.pos): 
                        print("lancer le jeu")
                        menu.son_bouton.play()
                        combat.afficher_fenetre()
                        # Ajoutez le code pour lancer le jeu ici
                    elif menu.ajouter_pokemon_rect.collidepoint(event.pos):
                        print("ajouter un pokemon")
                        menu.son_bouton.play()
                        ajouter.lancer()
                        
                    elif menu.pokedex_rect.collidepoint(event.pos):
                        print("pokedex")
                        menu.son_bouton.play()
                        acces_pokedex = Pokedex(800,800)
                        acces_pokedex.menuPokedex()

        menu.afficher_menu()
        pygame.display.flip()
        
if __name__ == "__main__":
    lancer_jeu()
