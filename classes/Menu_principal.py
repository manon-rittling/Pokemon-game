# importation des bibliothèques
import pygame
from pygame.locals import *



# classe Menu_principal
class Menu_principal:
    # constructeur de la classe
    def __init__(self):
        pygame.init()
        
        # Créer la fenêtre
        self.__fenetre = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Pokemon Arena-Fighter")
        pygame.display.set_icon(pygame.image.load("images/logo/logopokeball.png"))
        self.__bg = pygame.image.load("images/background/bg_menu_principal.png").convert()
        
    
        # cree titre du jeu
        self.__titre_principal = pygame.image.load("titre/Pokemon_titre.png").convert_alpha()
        self.__titre_principal_rect = self.__titre_principal.get_rect()
        self.__titre_principal_rect.x = 150
        self.__titre_principal_rect.y = -150

        # titre secondaire
        self.__titre_secondaire = pygame.image.load("titre/Arena1.png").convert_alpha()
        self.__titre_secondaire_rect = self.__titre_secondaire.get_rect()
        self.__titre_secondaire_rect.x = 243
        self.__titre_secondaire_rect.y = 165

        # Charger la police
        self.police = pygame.font.Font("police/pokemon Solid.ttf", 30)

    
        # Bouton lancer le jeu
        self.lancer_jeu = self.police.render("Lancer le jeu", True, (0, 0, 0))
        self.lancer_jeu_rect = self.lancer_jeu.get_rect()
        self.lancer_jeu_rect.x = 300
        self.lancer_jeu_rect.y = 260

        # Bouton ajouter pokemon
        
        self.ajouter_pokemon = self.police.render("Ajouter un pokemon", True, (0, 0, 0))
        self.ajouter_pokemon_rect = self.ajouter_pokemon.get_rect()
        self.ajouter_pokemon_rect.x = 300
        self.ajouter_pokemon_rect.y = 310

        # bouton pokedex
        self.pokedex = self.police.render("Pokedex", True, (0, 0, 0))
        self.pokedex_rect = self.pokedex.get_rect()
        self.pokedex_rect.x = 300
        self.pokedex_rect.y = 360

        self.couleur_origine = (55, 93, 170)
        self.couleur_changement = (255, 255, 255) 

    # ajout son boutons
        self.son_bouton = pygame.mixer.Sound("musique/voicy-pikachu01.mp3")

        pass
    # méthode afficher
    def afficher_menu(self):
        self.__fenetre.blit(self.__bg, (0, 0))
        self.__fenetre.blit(self.__titre_principal, self.__titre_principal_rect)
        self.__fenetre.blit(self.__titre_secondaire, self.__titre_secondaire_rect)
        
        if self.lancer_jeu_rect.collidepoint(pygame.mouse.get_pos()):
            self.lancer_jeu = self.police.render("Lancer le jeu", True, self.couleur_changement)
        else:
            self.lancer_jeu = self.police.render("Lancer le jeu", True, self.couleur_origine)
        self.__fenetre.blit(self.lancer_jeu, self.lancer_jeu_rect)

        if self.ajouter_pokemon_rect.collidepoint(pygame.mouse.get_pos()):
            self.ajouter_pokemon = self.police.render("Ajouter un pokemon", True, self.couleur_changement)
            
        else:
            self.ajouter_pokemon = self.police.render("Ajouter un pokemon", True, self.couleur_origine)
        self.__fenetre.blit(self.ajouter_pokemon, self.ajouter_pokemon_rect)

        if self.pokedex_rect.collidepoint(pygame.mouse.get_pos()):
            self.pokedex = self.police.render("Pokedex", True, self.couleur_changement)
        else:
            self.pokedex = self.police.render("Pokedex", True, self.couleur_origine)
        self.__fenetre.blit(self.pokedex, self.pokedex_rect)

        pygame.display.flip()