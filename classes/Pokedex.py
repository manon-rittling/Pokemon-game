import pygame as pg
import cv2
import numpy as np
import json
from classes.Menu_principal import *

with open("json/pokedex.json", "r") as fichier: # J'ouvre le fichier json
    donneesPokedex = json.load(fichier) # Je charge les données du fichier json dans une variable

class Pokedex: # Je crée une classe Pokedex
    def __init__(self, largeur, hauteur): # Je crée une méthode constructeur
        pg.init() # J'initialise pygame
        self.largeur = largeur # Je crée une variable largeur
        self.hauteur = hauteur # Je crée une variable hauteur
        self.fenetre = pg.display.set_mode((self.largeur, self.hauteur)) # Je crée une fenêtre
        pg.display.set_caption("Pokedex") # Je donne un titre à ma fenêtre
        pg.display.set_icon(pg.image.load("images/logo/logopokeball.png"))
        self.image_fond = pg.image.load("images/pokedex/paysage.jpg") # Je charge l'image de fond

        self.imagePokedex = pg.image.load("images/pokedex/pokedex1.png") # Je charge l'image du pokedex
        self.imagePokedex_redimensionnee = pg.transform.scale(self.imagePokedex, (800, 600)) # Je redimensionne l'image du pokedex

        self.imageTitrePokedex = pg.image.load("images/pokedex/titrePokedex.png") # Je charge l'image du titre du pokedex
        self.imageTitrePokedex_redimensionnee = pg.transform.scale(self.imageTitrePokedex, (300, 100)) # Je redimensionne l'image du titre du pokedex

        self.fleche_gauche = pg.Rect(110, 520, 50, 25) # Je crée un rectangle pour la flèche gauche
        self.fleche_droite = pg.Rect(175, 520, 50, 25) # Je crée un rectangle pour la flèche droite
        self.fleche_haut = pg.Rect(155, 475, 25, 50) # Je crée un rectangle pour la flèche haut
        self.fleche_bas = pg.Rect(155, 540, 25, 50) # Je crée un rectangle pour la flèche bas
        self.cercle = pg.draw.circle(self.fenetre, (255, 0, 0), (155, 520), 25) # Je crée un cercle

        self.couleur_fleche_gauche = (200, 0, 0) # Je crée une variable couleur pour la flèche gauche
        self.couleur_fleche_droite = (200, 0, 0) # Je crée une variable couleur pour la flèche droite
        self.couleur_fleche_haut = (200, 0, 0) # Je crée une variable couleur pour la flèche haut
        self.couleur_fleche_bas = (200, 0, 0) # Je crée une variable couleur pour la flèche bas
        self.couleur_cercle = (200, 0, 0) # Je crée une variable couleur pour le cercle

        self.son_clic = pg.mixer.Sound("musique/BEEP_touche.mp3") # Je charge le son du clic

        font_chemin = "police/Retro_Gaming.ttf" # Je crée une variable pour le chemin de la police
        font = pg.font.Font(font_chemin, 25) # Je crée une variable pour la police

        self.acces_pokedex = font.render("Pokedex", True, (255, 0, 0)) # Je crée une variable pour le texte "Pokedex"
        self.rect_acces_pokedex = self.acces_pokedex.get_rect(topleft=(270, 500)) # Je crée un rectangle pour le texte "Pokedex"
        self.revenir_menu_pokedex = font.render("Revenir au menu", True, (255, 0, 0)) # Je crée une variable pour le texte "Revenir au menu"
        self.rect_quitter_pokedex = self.revenir_menu_pokedex.get_rect(topleft=(270, 550)) # Je crée un rectangle pour le texte "Revenir au menu"

        self.retour_menu = font.render("Retour", True, (255, 0, 0)) # Je crée une variable pour le texte "Retour"
        self.rect_retour_menu = self.retour_menu.get_rect(topleft=(450, 620)) # Je crée un rectangle pour le texte "Retour"

        self.index_pokemon = 0 # Je crée une variable pour l'index du pokemon
        self.pokemon_affiche = 0 # Je crée une variable pour le pokemon affiché
        self.index_evolution = 0 # Je crée une variable pour l'index de l'évolution du pokemon

        self.afficher = True # Je crée une variable pour afficher la fenêtre


    def flouterImage(self, image): # Je crée une méthode pour flouter l'image
        image_np = pg.surfarray.array3d(image) # Je crée une variable pour l'image #surfarray.array3d(image) correspond à la conversion de l'image en tableau numpy
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR) # Je crée une variable pour l'image #cvtColor correspond à la méthode de conversion #RGB2BGR correspond à la conversion de RGB en BGR

        blurred_image = cv2.GaussianBlur(image_np, (25, 25), 0) # Je crée une variable pour l'image #cv2.GaussianBlur(image_np, (25, 25), 0) correspond à la conversion de l'image en flou #GaussianBlur correspond à la méthode de flou #25 correspond à la taille du flou #0 correspond à la valeur du flou

        blurred_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2RGB) 
        blurred_surface = pg.surfarray.make_surface(blurred_image) # Je crée une variable pour l'image #pg.surfarray.make_surface(blurred_image) correspond à la conversion de l'image en surface

        return blurred_surface # Je retourne l'image floutée #return correspond à la valeur de retour


    def diminuerLuminositeFleche(self, fleche): # Je crée une méthode pour diminuer la luminosité de la flèche (il me servira à faire un effet lorsque je clique dessus)
        border_radius = 5 # Je crée une variable pour le rayon de la bordure (afin de faire un effet de clique)
        fleche_couleur_temp = tuple(max(component - 50, 0) for component in self.couleur_fleche_bas) # Je crée une variable pour la couleur temporaire de la flèche
        pg.draw.rect(self.fenetre, fleche_couleur_temp, fleche, border_radius=border_radius) # Je crée un rectangle pour la flèche
        pg.display.flip() # Je rafraîchis l'écran
        pg.time.wait(100) # Je fais une pause de 100 millisecondes
        pg.draw.rect(self.fenetre, self.couleur_fleche_bas, fleche, border_radius=border_radius) # Je crée un rectangle pour la flèche


    def gererDéfilementPokemon(self): # Je crée une méthode pour gérer le défilement des pokemon
        
        font_chemin = "police/Retro_Gaming.ttf"
        font = pg.font.Font(font_chemin, 20)
        numero_pokemon = font.render(f"Numero : {donneesPokedex[self.pokemon_affiche]['numero']}", True, (0, 0, 0))
        self.fenetre.blit(numero_pokemon, (270, 440))
        
        for evenement in pg.event.get(): # Je crée une boucle pour les évènements
            if evenement.type == pg.QUIT: # Si l'évènement est de quitter
                self.afficher = False # Je crée une variable pour fermer la fenêtre #self.afficher = False correspond à la fermeture de la fenêtre
            elif evenement.type == pg.MOUSEBUTTONDOWN: # Si l'évènement est un clic de souris
                if evenement.button == 1: # Si le clic est un clic gauche #evenement.button == 1 correspond au clic gauche
                    if self.fleche_gauche.collidepoint(evenement.pos): # Si le clic est sur la flèche gauche #collidepoint correspond à la méthode pour vérifier si le clic est sur la flèche gauche
                        self.son_clic.play() # Je joue le son du clic
                        self.diminuerLuminositeFleche(self.fleche_gauche) # Je diminue la luminosité de la flèche gauche
                        self.afficherPokemonRencontre(self.index_pokemon - 1) # J'affiche le pokemon précédent
                        self.pokemon_affiche -= 1 # Je crée une variable pour le pokemon affiché #self.pokemon_affiche -= 1 correspond à l'index du pokemon affiché
                        if self.pokemon_affiche < 0: # Si le pokemon affiché est inférieur à 0
                            self.afficherPokemonRencontre(len(donneesPokedex) - 1) # J'affiche le dernier pokemon
                            self.pokemon_affiche = len(donneesPokedex) - 1 # self.pokemon_affiche = len(donneesPokedex) - 1 correspond à l'index du dernier pokemon
                        print("Clic gauche sur la flèche gauche") 
                    elif self.fleche_droite.collidepoint(evenement.pos):
                        self.son_clic.play()
                        self.diminuerLuminositeFleche(self.fleche_droite)
                        self.afficherPokemonRencontre(self.index_pokemon + 1)
                        self.pokemon_affiche += 1
                        if self.pokemon_affiche > len(donneesPokedex) - 1:
                            self.afficherPokemonRencontre(0)
                            self.pokemon_affiche = 0
                        print("Clic gauche sur la flèche droite")
                    elif self.fleche_haut.collidepoint(evenement.pos):
                        self.son_clic.play()
                        self.diminuerLuminositeFleche(self.fleche_haut)
                        
                        print("Clic gauche sur la flèche haut")
                    elif self.fleche_bas.collidepoint(evenement.pos):
                        self.son_clic.play()
                        self.diminuerLuminositeFleche(self.fleche_bas)
                       
                        print("Clic gauche sur la flèche bas")
                    elif self.cercle.collidepoint(evenement.pos):
                        self.cri_pokemon(self.index_pokemon)
                        print("Clic gauche sur le cercle")
                    elif self.rect_retour_menu.collidepoint(evenement.pos): # Si le clic est sur le texte "Retour"
                        self.son_clic.play() # Je joue le son du clic
                        self.menuPokedex()
                        if self.menuPokedex():
                            return "menu"
                        print("Clic gauche sur retour")


    def afficherPokemonRencontre(self, index_pokemon): # Je crée une méthode pour afficher le pokemon rencontré
        if 0 <= index_pokemon < len(donneesPokedex): # Si l'index du pokemon est compris entre 0 et le nombre de pokemon dans le pokedex
            self.index_pokemon = index_pokemon # Je crée une variable pour l'index du pokemon #self.index_pokemon = index_pokemon correspond à l'index du pokemon
            pokemon = donneesPokedex[index_pokemon] # Je crée une variable pour le pokemon #donneesPokedex[index_pokemon] correspond au pokemon

            if pokemon.get("visible", True): # Si le pokemon est visible
                try: # J'essaie de charger l'image du pokemon #try correspond à l'essai
                    chemin_image = pokemon["image"] # Je crée une variable pour le chemin de l'image du pokemon
                    image_pokemon = pg.image.load(chemin_image) # Je crée une variable pour l'image du pokemon
                    image_redimensionnee = pg.transform.scale(image_pokemon, (210, 210)) # Je crée une variable pour l'image du pokemon #pg.transform.scale(image_pokemon, (210, 210)) correspond à la redimension de l'image du pokemon
                    self.fenetre.blit(image_redimensionnee, (310, 125)) # J'affiche l'image du pokemon

                    font_chemin = "police/Retro_Gaming.ttf"
                    font = pg.font.Font(font_chemin, 16)

                    nom_pokemon = font.render(f"Nom : {pokemon['nom']}", True, (0, 0, 0))
                    self.fenetre.blit(nom_pokemon, (270, 470))

                    type_pokemon = font.render(f"Type : {pokemon['type']}", True, (0, 0, 0))
                    self.fenetre.blit(type_pokemon, (270, 500))

                    defense_pokemon = font.render(f"Défense : {pokemon['defense']}", True, (0, 0, 0))
                    self.fenetre.blit(defense_pokemon, (270, 530))

                    puissance_pokemon = font.render(f"Puissance d'attaque : {pokemon['puissance attaque']}", True, (0, 0, 0))
                    self.fenetre.blit(puissance_pokemon, (270, 560))

                    pointDeVie_pokemon = font.render(f"Point de vie : {pokemon['point de vie']}", True, (0, 0, 0))
                    self.fenetre.blit(pointDeVie_pokemon, (270, 590))

                except pg.error as e: # Si il y a une erreur de chargement d'image #pg.error correspond à l'erreur de pygame    
                    print(f"Erreur de chargement d'image : {e}")


    def cri_pokemon(self, index_pokemon): # Je crée une méthode pour le cri du pokemon
        if "cri" in donneesPokedex[index_pokemon]: # Si le cri du pokemon est dans les données du pokedex
            chemin_cri = donneesPokedex[index_pokemon]["cri"] # Je crée une variable pour le chemin du cri du pokemon
            cri = pg.mixer.Sound(chemin_cri) # Je crée une variable pour le cri du pokemon
            cri.play() # Je joue le cri du pokemon


    def afficherPokedex(self): # Je crée une méthode pour afficher le pokedex
        
        while self.afficher: # Tant que la variable pour afficher est vraie
            
            image_floue = self.flouterImage(self.image_fond) # J'appelle la méthode pour flouter l'image
            self.fenetre.blit(image_floue, (0, 0)) # J'affiche l'image floutée
            self.fenetre.blit(self.imagePokedex_redimensionnee, (0, 80)) # J'affiche l'image du pokedex
            self.afficherPokemonRencontre(self.pokemon_affiche) # J'appelle la méthode pour afficher le pokemon rencontré
            
            border_radius = 10 # Je crée une variable pour le rayon de la bordure
            pg.draw.rect(self.fenetre, self.couleur_fleche_gauche, self.fleche_gauche, border_radius=border_radius) # Je crée un rectangle pour la flèche gauche
            pg.draw.rect(self.fenetre, self.couleur_fleche_droite, self.fleche_droite, border_radius=border_radius)
            pg.draw.rect(self.fenetre, self.couleur_fleche_haut, self.fleche_haut, border_radius=border_radius)
            pg.draw.rect(self.fenetre, self.couleur_fleche_bas, self.fleche_bas, border_radius=border_radius)
            
            self.cercle = pg.draw.circle(self.fenetre, self.couleur_cercle, (705, 535), 35) # Bouton pour le cri du pokemon
            
            font_chemin = "police/Retro_Gaming.ttf" # Partie pour le bouton retour
            font = pg.font.Font(font_chemin, 16)
            retour = font.render(f"Retour", True, (0, 200, 0))
            self.fenetre.blit(retour, (450, 620))
            
            

            self.gererDéfilementPokemon() # J'appelle la méthode pour gérer le défilement des pokemon
            
            pg.display.flip()


    def menuPokedex(self):
        while self.afficher:
            image_floue = self.flouterImage(self.image_fond)
            self.fenetre.blit(image_floue, (0, 0))
            self.fenetre.blit(self.imagePokedex_redimensionnee, (0, 80))
            self.fenetre.blit(self.acces_pokedex, (270, 500))
            self.fenetre.blit(self.revenir_menu_pokedex, (270, 550))
            self.fenetre.blit(self.imageTitrePokedex_redimensionnee, (250, 185))
            
            border_radius = 10
            pg.draw.rect(self.fenetre, self.couleur_fleche_gauche, self.fleche_gauche, border_radius=border_radius)
            pg.draw.rect(self.fenetre, self.couleur_fleche_droite, self.fleche_droite, border_radius=border_radius)
            pg.draw.rect(self.fenetre, self.couleur_fleche_haut, self.fleche_haut, border_radius=border_radius)
            pg.draw.rect(self.fenetre, self.couleur_fleche_bas, self.fleche_bas, border_radius=border_radius)
            
            self.cercle = pg.draw.circle(self.fenetre, self.couleur_cercle, (705, 535), 35)

            for evenement in pg.event.get():
                if evenement.type == pg.QUIT:
                    self.afficher = False
                elif evenement.type == pg.MOUSEBUTTONDOWN:
                    if evenement.button == 1:
                        if self.rect_acces_pokedex.collidepoint(evenement.pos):
                            self.son_clic.play()
                            self.afficherPokedex()
                            print("Clic sur Pokedex")
                        elif self.rect_quitter_pokedex.collidepoint(evenement.pos):
                            self.son_clic.play()
                            print("Clic sur Quitter")
                            menu = Menu_principal()
                            menu.afficher_menu()
                            self.afficher = False

            pg.display.flip()


if __name__ == "__main__": # Si le fichier est exécuté
    fenetre = Pokedex(800, 800) # Je crée une variable pour la fenêtre
    fenetre.menuPokedex() # J'appelle la méthode pour le menu du pokedex