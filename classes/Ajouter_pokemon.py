
import pygame
from pygame.locals import *
import sys
import json
from classes.Menu_principal import *


class Ajouter_pokemon:
    def __init__(self):
        
        # Initialisation de pygame
        pygame.init()
        
        # Crée la fenêtre
        self.fenetre = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Ajouter un Pokémon")
        pygame.display.set_icon(pygame.image.load("images/logo/logopokeball.png"))
        
        # Horloge
        self.clock = pygame.time.Clock()

        # Chargement du fond, du titre, de la police, du cadre de texte
        self.bg = pygame.image.load("images/background/bg_ajout_pokemon1.png").convert()
        self.titre = pygame.image.load("titre/ajoute_ton_pokemon.png").convert_alpha()
        self.police = pygame.font.Font("police/Pokemon Solid.ttf", 30)
        self.police2 = pygame.font.Font("police/Retro_gaming.ttf", 15)
        self.cadre_texte = pygame.image.load("images/cadre_texte/cadre_texte1.png").convert_alpha()

        # Chargement des silhouettes
        self.silhouettes = [
            pygame.image.load("images/pokemon/roucool1.png").convert_alpha(),
            pygame.image.load("images/pokemon/rattata1.png").convert_alpha(),
            pygame.image.load("images/pokemon/osselait1.png").convert_alpha()
        ]

        # Positions des silhouettes
        self.positions_silhouettes = [
            (70, 380),
            (300, 380),
            (570, 380)
        ]

        # ellipse pour les silhouettes
        self.ellipse_silhouettes = [pygame.Rect(pos, (self.silhouettes[i].get_width(), self.silhouettes[i].get_height())) for i, pos in enumerate(self.positions_silhouettes)]

        # Initialisation des attributs
        self.nom = [
            "Roucool",
            "Rattata",
            "Osselait"
        ]
        self.type = [
            "vol",
            "Normal",
            "sol"
        ]

        self.vie = [ 45, 50, 45]
        self.niveau = [5, 6, 5]
        self.attaque = [60, 55,45]
        self.defense = [25, 30, 50]
        self.xp = [0,0,0]

        self.index_pokemon = None   
        self.surbrillance_silhouette = None  
        self.message_affiche = False
        

    
            

    def pour_ajouter_fichier(self):
        # enrigister dans le fichier pokemon.json
        if self.index_pokemon is not None:
            
            with open("json/pokemon.json", "r") as f:
                pokemon = json.load(f)

            # verifier si pokemon existe deja
                for p in pokemon:
                    if p["nom"] == self.nom[self.index_pokemon]:
                        return

            nouveau_pokemon = {
                "nom": self.nom[self.index_pokemon],
                "type": self.type[self.index_pokemon],
                "pv": self.vie[self.index_pokemon],
                "lvl": self.niveau[self.index_pokemon],
                "attaque": self.attaque[self.index_pokemon],
                "defense": self.defense[self.index_pokemon],
                "xp": self.xp[self.index_pokemon],
                "xp_necessaire": 50,
                "image": f"images/pokemon/{self.nom[self.index_pokemon]}.png"
            }

            pokemon.append(nouveau_pokemon)

            with open("json/pokemon.json", "w") as f:
                json.dump(pokemon, f, indent=-1)

            
            self.message_affiche = True
            
    def gerer_evenements(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEMOTION:
                self.surbrillance_silhouette = None  # Réinitialise la surbrillance
                for i, rect in enumerate(self.ellipse_silhouettes):
                    if rect.collidepoint(event.pos):
                        # La souris est sur la silhouette
                        self.surbrillance_silhouette = i

            elif event.type == MOUSEBUTTONDOWN:
                for i, rect in enumerate(self.ellipse_silhouettes):
                    if rect.collidepoint(event.pos):
                        self.index_pokemon = i
                        
                        self.pour_ajouter_fichier()
                        
                        self.message_affiche = True
                        break
               
            elif event.type == KEYDOWN:
                    if event.key == K_RETURN:

                        menu = Menu_principal()
                        menu.afficher_menu()
                        self.message_affiche = False
                        if menu:
                            return "menu"

        
        pygame.display.flip()
            
    def afficher(self):
        # Affiche le fond, le titre
        self.fenetre.blit(self.bg, (0, 0))
        self.fenetre.blit(self.titre, (110, 240))

        # Affiche les silhouettes
        for i, silhouette in enumerate(self.silhouettes):
            if self.surbrillance_silhouette == i:
                # Ajoute une surbrillance si la souris est sur la silhouette
                pygame.draw.ellipse(self.fenetre, (255, 204, 1), (self.positions_silhouettes[i][0] - 10, self.positions_silhouettes[i][1] - 5, silhouette.get_width() + 20, silhouette.get_height() + 20), 5)
            self.fenetre.blit(silhouette, self.positions_silhouettes[i])

        # Affiche le cadre de texte
        for i in range(3):
            self.fenetre.blit(self.cadre_texte, (20 + i * 270, 530))

        # Affiche les informations du premier Pokémon
        self.texte = self.police2.render(f"Nom : {self.nom[0]}", True, (0, 0, 0))
        self.fenetre.blit(self.texte, (50, 565))
        self.texte = self.police2.render(f"Type : {self.type[0]}", True, (0, 0, 0))
        self.fenetre.blit(self.texte, (50, 595))
        self.texte = self.police2.render(f"Vie : {self.vie[0]}", True, (0, 0, 0))
        self.fenetre.blit(self.texte, (50, 625))
        self.texte = self.police2.render(f"Niveau : {self.niveau[0]}", True, (0, 0, 0))
        self.fenetre.blit(self.texte, (50, 655))
        self.texte = self.police2.render(f"Attaque : {self.attaque[0]}", True, (0, 0, 0))
        self.fenetre.blit(self.texte, (50, 685))
        self.texte = self.police2.render(f"Défense : {self.defense[0]}", True, (0, 0, 0))
        self.fenetre.blit(self.texte, (50, 715))

        # Affiche les informations du deuxième Pokémon
        self.texte = self.police2.render(f"Nom : {self.nom[1]}", True, (0, 0, 0))
        self.fenetre.blit(self.texte, (320, 565))
        self.texte = self.police2.render(f"Type : {self.type[1]}", True, (0, 0, 0))
        self.fenetre.blit(self.texte, (320, 595))
        self.texte = self.police2.render(f"Vie : {self.vie[1]}", True, (0, 0, 0))
        self.fenetre.blit(self.texte, (320, 625))
        self.texte = self.police2.render(f"Niveau : {self.niveau[1]}", True, (0, 0, 0))
        self.fenetre.blit(self.texte, (320, 655))
        self.texte = self.police2.render(f"Attaque : {self.attaque[1]}", True, (0, 0, 0))
        self.fenetre.blit(self.texte, (320, 685))
        self.texte = self.police2.render(f"Défense : {self.defense[1]}", True, (0, 0, 0))
        self.fenetre.blit(self.texte, (320, 715))

        # Affiche les informations du troisième Pokémon
        self.texte = self.police2.render(f"Nom : {self.nom[2]}", True, (0, 0, 0))
        self.fenetre.blit(self.texte, (590, 565))
        self.texte = self.police2.render(f"Type : {self.type[2]}", True, (0, 0, 0))
        self.fenetre.blit(self.texte, (590, 595))
        self.texte = self.police2.render(f"Vie : {self.vie[2]}", True, (0, 0, 0))
        self.fenetre.blit(self.texte, (590, 625))
        self.texte = self.police2.render(f"Niveau : {self.niveau[2]}", True, (0, 0, 0))
        self.fenetre.blit(self.texte, (590, 655))
        self.texte = self.police2.render(f"Attaque : {self.attaque[2]}", True, (0, 0, 0))
        self.fenetre.blit(self.texte, (590, 685))
        self.texte = self.police2.render(f"Défense : {self.defense[2]}", True, (0, 0, 0))
        self.fenetre.blit(self.texte, (590, 715))

        # Affiche le message si nécessaire
        if self.message_affiche:
                    self.texte = self.police.render(f"Le Pokémon {self.nom[self.index_pokemon]} a été ajouté !", True, (0, 0, 0))
                    self.fenetre.blit(self.texte, (200, 350))

        

               
    def lancer(self):
        while True:
            
            resultat = self.gerer_evenements()
            if resultat == "menu":
                return
            self.afficher()
            self.clock.tick(60)
            
               

if __name__ == "__main__":
    ajouter = Ajouter_pokemon()
    ajouter.lancer()