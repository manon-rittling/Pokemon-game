import pygame as pg
import cv2
# import numpy as np
import json
import random
from classes.Pokemon import *
from classes.Combat import *
from classes.Menu_principal import *

# with open("json/pokemon.json", "r") as fichier: # Ouvrir le fichier JSON en lecture seule et en mode texte (r) et écriture (w) 
#     donneesPokemon = json.load(fichier)


infoPokemon = Pokemon.import_json("json/pokemon.json") # Importer les données du fichier JSON

class Nouvelle_partie:

    
    def __init__(self, largeur, hauteur):
        pg.init()
        self.largeur = largeur
        self.hauteur = hauteur
        self.fenetre = pg.display.set_mode((self.largeur, self.hauteur))
        pg.display.set_caption("Pokemon Arena-Fighter") # Titre de la fenêtre
        pg.display.set_icon(pg.image.load("images/logo/logopokeball.png")) # Icone de la fenêtre
        self.image_fond = pg.image.load("images/background/paysage_pokemon_nouvelle_partie.jpg") # Image de fond
        self.image_fond_redimensionne = pg.transform.scale(self.image_fond, (800, 800)) # Redimensionner l'image de fond

        self.image_carte_pokemon = pg.image.load("images/background/cadre carte vide.png") # Image de la carte Pokémon
        self.image_carte_pokemon_redimensionne = pg.transform.scale(self.image_carte_pokemon, (450, 620))

        font_chemin = "police/Pokemon Solid.ttf" # Chemin de la police
        font = pg.font.Font(font_chemin, 30) # Police et taille de la police

        self.nom_dresseur = pg.image.load("titre/nom-dresseur.png")
        self.nom_dresseur = pg.transform.scale(self.nom_dresseur, (400, 100))
        
        self.input_box = pg.Rect(300, 100, 270, 40) # Position et taille de la zone de texte pour écrire le nom du dresseur
        self.is_input_active = False 
        self.texte = "" # Texte à écrire dans la zone de texte
        self.font = pg.font.Font(None, 36)

        self.fleche_gauche = pg.image.load("images/bouton/fleche-gauche.png") # Image de la flèche gauche
        self.fleche_gauche = pg.transform.scale(self.fleche_gauche, (40, 40))

        self.fleche_droite = pg.image.load("images/bouton/fleche-droite.png") # Image de la flèche droite
        self.fleche_droite = pg.transform.scale(self.fleche_droite, (40, 40))
       

        self.index_pokemon = 0 # Index du Pokémon actuellement affiché

        self.equipe_pokemon = [] # Liste des Pokémon dans l'équipe du joueur

    def mise_a_jour_fichier_json(self): # Mettre à jour le fichier JSON # Actuellement inutilisé
        Pokemon.import_json("json/pokemon.json")

        
    def flouterImage(self, image): # Flouter l'image de fond
        image_np = pg.surfarray.array3d(image) # Je convertis la surface Pygame en tableau numpy
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)  # Je convertis l'image en BGR

        blurred_image = cv2.GaussianBlur(image_np, (25, 25), 0) # Je floute l'image avec un noyau de 25x25 # Un noyau plus grand donne un flou plus important

        blurred_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2RGB) # Je reconverti l'image en RGB #RGB signifie Rouge, Vert, Bleu
        blurred_surface = pg.surfarray.make_surface(blurred_image) # Je reconverti l'image en surface Pygame

        return blurred_surface # Je retourne l'image floutée
    
    def fenetre_ecrire_nom(self): # Afficher la fenêtre pour écrire le nom du dresseur
        pg.draw.rect(self.fenetre, (255, 255, 255), self.input_box, 2) # Rectangle blanc pour la zone de texte , 2 pour l'épaisseur de la bordure
        texte_surface = self.font.render(self.texte, True, (200, 0, 0))
        width = max(200, texte_surface.get_width() + 10) # .Get_width() + 10 pour que la zone de texte soit plus grande que le texte
        self.input_box.w = width # Largeur de la zone de texte
        self.fenetre.blit(texte_surface, (self.input_box.x + 5, self.input_box.y + 5))

    def zone_texte(self, event): # Zone de texte pour écrire le nom du dresseur

        if event.type == pg.MOUSEBUTTONDOWN: # Si on clique
            if self.input_box.collidepoint(event.pos): # Si on clique sur la zone de texte .collidepoint() permet de savoir si un point est dans un rectangle
                self.is_input_active = not self.is_input_active # Activer ou désactiver la zone de texte
            else:
                self.is_input_active = False # Désactiver la zone de texte

        if event.type == pg.KEYDOWN: # Si on appuie sur une touche
            if self.is_input_active: # Si la zone de texte est active
                if event.key == pg.K_RETURN: # Si on appuie sur la touche entrée
                    print(self.texte) # Afficher le texte
                    self.texte = "" # Réinitialiser le texte
                elif event.key == pg.K_BACKSPACE: # Si on appuie sur la touche retour
                    self.texte = self.texte[:-1] # Supprimer le dernier caractère
                else:
                    self.texte += event.unicode # Ajouter le caractère à la fin du texte

    def afficherPokemon(self, index_pokemon): # Afficher les informations du Pokémon
        
        
        if 0 <= index_pokemon < len(Pokemon.tous_pokemons): # Si l'index du pokémon est dans la liste des pokémons
            self.index_pokemon = index_pokemon # Mettre à jour l'index du pokémon
            pokemon = infoPokemon[self.index_pokemon]  # Obtenir l'objet Pokemon spécifique

            try: # Essayer de charger l'image du Pokémon
                # Charger et afficher l'image du Pokémon
                image_pokemon = pg.image.load(f"images/pokemon/{pokemon.nom}1.png")
                image_redimensionnee = pg.transform.scale(image_pokemon, (270, 270))
                self.fenetre.blit(image_redimensionnee, (270, 240))

                # Afficher le nom du Pokémon
                font_chemin_nom = "police/Retro_Gaming.ttf"
                font_nom = pg.font.Font(font_chemin_nom, 30)
                nom_pokemon = font_nom.render(f"{pokemon.nom}", True, (0, 0, 0))
                self.fenetre.blit(nom_pokemon, (300, 185))

                # Afficher le type du Pokémon
                font_chemin_type = "police/Retro_Gaming.ttf"
                font_type = pg.font.Font(font_chemin_type, 20)
                type_pokemon = font_type.render(f"Type : {pokemon.type.nom}", True, (0, 0, 0))
                self.fenetre.blit(type_pokemon, (310, 525))

                # Afficher les autres attributs du Pokémon
                font_chemin_info = "police/Retro_Gaming.ttf"
                font_info = pg.font.Font(font_chemin_info, 16)
                defense_pokemon = font_info.render(f"Défense : {pokemon.defense}", True, (0, 0, 0))
                self.fenetre.blit(defense_pokemon, (220, 580))
                puissance_pokemon = font_info.render(f"Puissance d'attaque : {pokemon.attaque}", True, (0, 0, 0))
                self.fenetre.blit(puissance_pokemon, (220, 640))
                pointDePV_pokemon = font_info.render(f"Point de PV : {pokemon.pv}", True, (0, 0, 0))
                self.fenetre.blit(pointDePV_pokemon, (220, 700))

                # Afficher les boutons de navigation
                self.fenetre.blit(self.fleche_gauche, (200, 400))
                self.fenetre.blit(self.fleche_droite, (550, 400))
                lancer_partie = font_info.render(f"Lancer", True, (0, 200, 0))
                self.fenetre.blit(lancer_partie, (535, 743))

                ajout_pokemon = font_info.render(f"Ajouter", True, (0, 200, 0))
                self.fenetre.blit(ajout_pokemon, (530, 643))


                chemin_bouton_retour = "images/bouton/bouton-retour.png"
                bouton_retour = pg.image.load(chemin_bouton_retour)
                bouton_retour_redimensionne = pg.transform.scale(bouton_retour, (110, 50))
                self.fenetre.blit(bouton_retour_redimensionne, (680, 720))

            except pg.error as e:
                print(f"Erreur de chargement d'image : {e}") # Afficher l'erreur si le chargement de l'image échoue

    
    def choix_pokemon_aleatoire(self): 
        # Sélectionnez un objet Pokemon aléatoire de la liste
        donnees_pokemon_aleatoire = random.choice(Pokemon.tous_pokemons)

        # Créez une nouvelle instance du Pokémon
        pokemon_aleatoire = Pokemon(
            nom=donnees_pokemon_aleatoire.nom,
            type_pokemon=donnees_pokemon_aleatoire.type,
            pv=donnees_pokemon_aleatoire.pv,
            attaque=donnees_pokemon_aleatoire.attaque,
            defense=donnees_pokemon_aleatoire.defense,
            lvl=donnees_pokemon_aleatoire.lvl,
            xp=donnees_pokemon_aleatoire.xp,
            xp_necessaire=donnees_pokemon_aleatoire.xp_necessaire,
            attaque_de_base=donnees_pokemon_aleatoire.attaque_de_base or Attaque.assigner_attaque_base(donnees_pokemon_aleatoire)
        )

        # Mettre à jour le statut "visible" dans pokedex.json
        with open("json/pokedex.json", "r") as fichier:
            donnees_pokedex = json.load(fichier)

        for pokemon in donnees_pokedex:
            if pokemon["nom"] == pokemon_aleatoire.nom:
                pokemon["visible"] = True
                break

        with open("json/pokedex.json", "w") as fichier:
            json.dump(donnees_pokedex, fichier, indent=2)

        return pokemon_aleatoire


    def choix_pokemon_joueur(self): # Choisir un Pokémon pour le joueur
        pokemon_joueur = infoPokemon[self.index_pokemon] # Obtenir l'objet Pokemon spécifique
        
        print(f"Pokemon choisi par le joueur : {pokemon_joueur.nom}") # Afficher le nom du Pokémon choisi par le joueur

        # Charger les données du Pokédex depuis le fichier JSON
        with open("json/pokedex.json", "r") as fichier:
            donnees_pokedex = json.load(fichier)

        # Mettre à jour la visibilité du Pokémon choisi par le joueur
        index_pokemon_joueur = self.index_pokemon
        donnees_pokedex[index_pokemon_joueur]["visible"] = True

        # Sauvegarder les données mises à jour dans le fichier JSON
        with open("json/pokedex.json", "w") as fichier:
            json.dump(donnees_pokedex, fichier, indent=2)

        return pokemon_joueur
    
    def creer_equipe(self):
        pokemon_choisi = self.choix_pokemon_joueur()
        
        # Assurez-vous que le Pokémon a une attaque de base assignée
        if pokemon_choisi.attaque_de_base is None:
            pokemon_choisi.attaque_de_base = Attaque.assigner_attaque_base(pokemon_choisi)

        self.equipe_pokemon.append(pokemon_choisi)
        print(f"Pokémon ajouté à l'équipe de {self.texte} : {pokemon_choisi.nom}")
        return self.equipe_pokemon


    def afficher_fenetre(self): # Afficher la fenêtre ### METHODE PRINCIPALE ###
        
        while True:
            image_floue = self.flouterImage(self.image_fond_redimensionne)
            self.fenetre.blit(image_floue, (0, 0))
            self.fenetre.blit(self.nom_dresseur, (200, 20))
            self.fenetre.blit(self.image_carte_pokemon_redimensionne, (180, 170))
            self.fenetre_ecrire_nom()
            self.afficherPokemon(self.index_pokemon)
            

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

                self.zone_texte(event)

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Bouton pour choisir un Pokémon précédent
                        if 200 <= event.pos[0] <= 240 and 400 <= event.pos[1] <= 440:
                            self.afficherPokemon(self.index_pokemon - 1)
                        # Bouton pour choisir un Pokémon suivant
                        elif 550 <= event.pos[0] <= 590 and 400 <= event.pos[1] <= 440:
                            self.afficherPokemon(self.index_pokemon + 1)
                        # Bouton pour ajouter le Pokémon à l'équipe
                        elif 530 <= event.pos[0] <= 600 and 643 <= event.pos[1] <= 660:
                            print("Pokemon ajouté à l'équipe")
                            equipe = self.creer_equipe()
                            print("Équipe actuelle :", [pokemon.nom for pokemon in equipe])
                        # Bouton pour lancer un combat
                        elif 535 <= event.pos[0] <= 600 and 743 <= event.pos[1] <= 760:
                            pokemon_joueur = self.creer_equipe()[0]
                            pokemon_aleatoire = self.choix_pokemon_aleatoire()
                            if pokemon_joueur.attaque_de_base is None:
                                pokemon_joueur.attaque_de_base = Attaque.assigner_attaque_base(pokemon_joueur)
                            if pokemon_aleatoire.attaque_de_base is None:
                                pokemon_aleatoire.attaque_de_base = Attaque.assigner_attaque_base(pokemon_aleatoire)

                            combat = Combat(self) 
                            combat.lancer_combat(pokemon_joueur, pokemon_aleatoire)
                            self.equipe_pokemon = [] # Je vide l'équipe du joueur après le combat
                            return True 
                            
                        # Bouton pour retourner au menu
                        elif 680 <= event.pos[0] <= 790 and 720 <= event.pos[1] <= 770:
                            print("Retour")
                            menu = Menu_principal()
                            menu.afficher_menu()
                            if menu:
                                return "menu"

            pg.display.flip()


if __name__ == "__main__": # Si le fichier est exécuté directement
    nouvelle_partie = Nouvelle_partie(800, 800) # Créer une nouvelle instance de la classe Nouvelle_partie
    nouvelle_partie.afficher_fenetre() # Afficher la fenêtre