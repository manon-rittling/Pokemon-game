import pygame
import pygame.time
from classes.Menu_principal import *
import random

class Combat:
    XP_PAR_VICTOIRE = 20

    def __init__(self, nouvelle_partie=None):
        self.running = True
        self.tour_mon_pokemon = True
        self.mon_pokemon = None
        self.adversaire = None
        self.derniere_attaque = 0  # Temps de la dernière attaque en millisecondes
        self.nouvelle_partie = nouvelle_partie

    @staticmethod
    def calculer_degats(attaquant, attaque, defenseur):
        coefficient_eff = 1.0
        if attaque.type.nom in defenseur.type.faiblesses:
            coefficient_eff = 2
        elif attaque.type.nom in defenseur.type.forces:
            coefficient_eff = 0.5
        elif attaque.type.nom in defenseur.type.nulle_defense:
            coefficient_eff = 0.0

        degats = int((((attaquant.lvl * 0.4 + 2) * attaquant.attaque * attaque.puissance / (defenseur.defense * 50)) + 2)) * coefficient_eff
        return degats

    @staticmethod
    def appliquer_degats(defenseur, degats):
        defenseur.pv -= int(degats)
        if defenseur.pv < 0:
            defenseur.pv = 0
        return defenseur.pv

    def dessiner_bouton(self, ecran, message, x, y, largeur, hauteur, couleur_inactive, couleur_active, border_radius=10):
        souris = pygame.mouse.get_pos()
        rect = pygame.Rect(x, y, largeur, hauteur)

        if rect.collidepoint(souris[0], souris[1]):
            pygame.draw.rect(ecran, couleur_active, rect, border_radius=border_radius)
        else:
            pygame.draw.rect(ecran, couleur_inactive, rect, border_radius=border_radius)

        font = pygame.font.Font("police/Retro_Gaming.ttf", 15)
        text = font.render(message, True, (0, 0, 0))
        ecran.blit(text, (x + (largeur / 2 - text.get_width() / 2), y + (hauteur / 2 - text.get_height() / 2)))

        return rect  # Retourner le rectangle représentant le bouton

    def afficher_message(self, ecran, message):
        font = pygame.font.Font("police/Retro_Gaming.ttf", 17)
        # Dessiner un rectangle de fond pour effacer le vieux message
        message_background = pygame.Rect(0, 550, 800, 50)  # Ajustez la taille au besoin
        pygame.draw.rect(ecran, (0, 0, 0), message_background)
        texte = font.render(message, True, (255, 255, 255))
        ecran.blit(texte, (400 - texte.get_width() // 2, 550))
        pygame.display.flip()
        pygame.time.delay(1000)  # Délai pour que le message soit visible

    def effacer_message(self, ecran):
        message_background = pygame.Rect(0, 550, 800, 50)  # Ajustez la taille au besoin
        pygame.draw.rect(ecran, (0, 0, 0), message_background)  # Utilisez la couleur de l'arrière-plan
        pygame.display.flip()

    def afficher_dialogue_fin_combat(self, ecran):
        while True:
            # Dessiner le message
            self.afficher_message(ecran, "Voulez-vous recommencer un combat ?")

            # Récupérer les coordonnées et les dimensions des boutons "Oui" et "Non"
            bouton_oui_rect = self.dessiner_bouton(ecran, "Oui", 50, 500, 100, 50, (0, 255, 0), (100, 255, 100))
            bouton_non_rect = self.dessiner_bouton(ecran, "Non", 650, 500, 100, 50, (255, 0, 0), (255, 100, 100))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_oui_rect.collidepoint(event.pos):
                        # Relancer un nouveau combat
                        return True
                    elif bouton_non_rect.collidepoint(event.pos):
                        # Retourner au menu principal
                        return False

            pygame.display.flip()

    def choisir_pokemon(self, ecran):
        equipe = self.nouvelle_partie.equipe_pokemon # Récupérer l'équipe du joueur

        pokemon_choisi = None
        while not pokemon_choisi:
            background_image = pygame.image.load("images/background/choix.png")
            background_image = pygame.transform.scale(background_image, (400, 300))  # Redimensionner l'image

            liste_rect = pygame.Rect(200, 100, 400, 300)
            # Dessiner l'image d'arrière-plan pour le rectangle
            ecran.blit(background_image, (200, 100))

            font_titre = pygame.font.Font("police/Retro_Gaming.ttf", 18)
            texte_titre = font_titre.render("Choisir un Pokémon:", True, (255, 255, 255))
            ecran.blit(texte_titre, (285, 110))

            font = pygame.font.Font("police/Retro_Gaming.ttf", 16)
            for i, pokemon in enumerate(equipe):    # Afficher les noms des Pokémon
                texte_pokemon = font.render(pokemon.nom, True, (255, 255, 255))
                rect_pokemon = pygame.Rect(345, 140 + i * 20, 150, 20)
                souris_x, souris_y = pygame.mouse.get_pos()  # Récupérer les coordonnées de la souris
                if rect_pokemon.collidepoint(souris_x, souris_y):
                    texte_pokemon = font.render(pokemon.nom, True, (255, 255, 0))  # Texte en jaune
                #pygame.draw.rect(ecran, (200, 200, 200), rect_pokemon)
                ecran.blit(texte_pokemon, (345, 140 + i * 20))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, pokemon in enumerate(equipe):
                        rect_pokemon = pygame.Rect(345, 140 + i * 20, 150, 20)
                        if rect_pokemon.collidepoint(event.pos):
                            pokemon_choisi = pokemon
                            break

        return pokemon_choisi



    def lancer_combat(self, mon_pokemon, adversaire):
        self.mon_pokemon = mon_pokemon 
        self.adversaire = adversaire
        self.running = True 
        self.tour_mon_pokemon = True 
        pygame.init() 
        pygame.mixer.init() 
        pygame.mixer.music.load('musique/ostbattle.mp3') # Charger la musique de combat
        pygame.mixer.music.play(-1)  # -1 signifie que la musique va boucler
        ecran = pygame.display.set_mode((800, 600))
        sprite_mon_pokemon = pygame.image.load(f"images/pokemon_de_dos/{mon_pokemon.nom}1.png") # Charger le sprite du Pokémon du joueur
        sprite_adversaire = pygame.image.load(f"images/pokemon/{adversaire.nom}1.png") # Charger le sprite du Pokémon adverse
        arriere_plan = pygame.image.load('images/background/bg_areneCombat.png')
        font = pygame.font.Font("police/Retro_Gaming.ttf", 18)
        clock = pygame.time.Clock()
        taille_sprite_mon_pokemon = (190, 190) 
        taille_sprite_adversaire = (160, 160)
        sprite_mon_pokemon = pygame.transform.scale(sprite_mon_pokemon, taille_sprite_mon_pokemon)
        sprite_adversaire = pygame.transform.scale(sprite_adversaire, taille_sprite_adversaire)

        # Définir les rectangles pour les boutons
        bouton_attaque_rect = pygame.Rect(50, 500, 100, 50)
        bouton_fuite_rect = pygame.Rect(650, 500, 100, 50)
        bouton_choix_pokemon_rect = pygame.Rect(270, 500, 250, 50)

        while self.running:
            self.effacer_message(ecran) # Effacer le message précédent
            ecran.blit(arriere_plan, (0, 0))  # Dessiner l'arrière-plan
            ecran.blit(sprite_mon_pokemon, (50, 280)) # Dessiner le sprite du Pokémon du joueur
            ecran.blit(sprite_adversaire, (600, 100)) # Dessiner le sprite du Pokémon adverse
            self.dessiner_bouton(ecran, "Attaquer", 50, 500, 100, 50, (255, 0, 0), (255, 100, 100))
            self.dessiner_bouton(ecran, "Fuite", 650, 500, 100, 50, (255, 0, 0), (255, 100, 100))
            self.dessiner_bouton(ecran, "Changer de Pokemon", 270, 500, 250, 50, (255, 0, 0), (255, 100, 100))

            # Mettre à jour l'affichage des PV pour les deux Pokémon, avoir les informations à jour
            self.mettre_a_jour_info_pokemon(ecran, font, self.mon_pokemon, self.adversaire)

            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_attaque_rect.collidepoint(event.pos) and self.tour_mon_pokemon:
                        if self.mon_pokemon.pv > 0: # Vérifier si le Pokémon du joueur est toujours en vie
                            message = self.effectuer_attaque(self.mon_pokemon, self.adversaire) # Effectuer une attaque
                            self.afficher_message(ecran, message)
                            self.tour_mon_pokemon = False
                    elif bouton_choix_pokemon_rect.collidepoint(event.pos): # Choisir un autre Pokémon
                        self.mon_pokemon = self.choisir_pokemon(ecran) 
                        if self.mon_pokemon:  # Si un Pokémon a été choisi
                            sprite_mon_pokemon = pygame.image.load(f"images/pokemon_de_dos/{self.mon_pokemon.nom}1.png") # Charger le sprite du Pokémon choisi
                            sprite_mon_pokemon = pygame.transform.scale(sprite_mon_pokemon, taille_sprite_mon_pokemon) 
                            self.tour_mon_pokemon = True # C'est le tour du joueur
                    elif bouton_fuite_rect.collidepoint(event.pos): # Fuir le combat
                        self.gerer_action_bouton_fuite(ecran)
                        self.soigner_pokemons()
                        menu = Menu_principal() 
                        menu.afficher_menu() # Retourner au menu principal
                        if menu:
                            return "menu" 

            pygame.display.flip()

            if not self.tour_mon_pokemon and self.adversaire.pv > 0: # Si c'est le tour du Pokémon adverse et qu'il est toujours en vie
                message = self.effectuer_attaque(self.adversaire, self.mon_pokemon) # Effectuer une attaque
                self.afficher_message(ecran, message) 
                self.tour_mon_pokemon = True
                self.mettre_a_jour_info_pokemon(ecran, font, self.mon_pokemon, self.adversaire)

            if self.mon_pokemon.pv <= 0 and not self.verifier_pokemon_restants(self.nouvelle_partie.equipe_pokemon): # Si tous les Pokémon du joueur sont hors de combat
                self.afficher_message(ecran, "Tous vos Pokémon sont hors de combat !")
                self.soigner_pokemons() # Soigner tous les Pokémon du joueur et de l'adversaire
                choix_recommencer = self.afficher_dialogue_fin_combat(ecran)
                self.mettre_a_jour_info_pokemon(ecran, font, self.mon_pokemon, self.adversaire)
            
                if choix_recommencer: # Si le joueur veut recommencer un combat après avoir perdu
                    nouveau_adversaire = self.nouvelle_partie.choix_pokemon_aleatoire() # Choisir un Pokémon aléatoire pour le combat
                    if nouveau_adversaire == self.mon_pokemon: 
                        nouveau_adversaire = self.nouvelle_partie.choix_pokemon_aleatoire()
                    self.lancer_combat(self.mon_pokemon, nouveau_adversaire)
                else:
                    self.mettre_a_jour_info_pokemon(ecran, font, self.mon_pokemon, self.adversaire) 
                    self.running = False
                    menu = Menu_principal()
                    menu.afficher_menu()
                    pygame.mixer.music.stop()
                    return "menu"
            elif self.adversaire.pv <= 0: # Si le Pokémon adverse est hors de combat
                self.mettre_a_jour_info_pokemon(ecran, font, self.mon_pokemon, self.adversaire)
                self.afficher_message(ecran, f"{self.adversaire.nom} est hors de combat !")
                self.soigner_pokemons()
                self.mon_pokemon.gagner_xp(Combat.XP_PAR_VICTOIRE)
                self.soigner_pokemons() # Soigner tous les Pokémon du joueur et de l'adversaire
                choix_recommencer = self.afficher_dialogue_fin_combat(ecran)
            
                if choix_recommencer: # Si le joueur veut recommencer un combat après avoir gagné
                    nouveau_adversaire = self.nouvelle_partie.choix_pokemon_aleatoire()
                    if nouveau_adversaire == self.mon_pokemon:
                        nouveau_adversaire = self.nouvelle_partie.choix_pokemon_aleatoire()
                    self.lancer_combat(self.mon_pokemon, nouveau_adversaire)
                else:
                    self.mettre_a_jour_info_pokemon(ecran, font, self.mon_pokemon, self.adversaire) 
                    self.running = False
                    menu = Menu_principal()
                    menu.afficher_menu()
                    pygame.mixer.music.stop()
                    return "menu"

    def soigner_pokemons(self): # Soigner tous les Pokémon du joueur et de l'adversaire grâce à la méthode soigner de la classe Pokemon
        """Soigner tous les Pokémon de l'équipe du joueur."""
        for pokemon in self.nouvelle_partie.equipe_pokemon:
            pokemon.soigner()
        self.adversaire.soigner()


    def verifier_pokemon_restants(self, equipe):
        """Vérifie si au moins un Pokémon dans l'équipe a des PV supérieurs à 0."""
        return any(pokemon.pv > 0 for pokemon in equipe)

    def mettre_a_jour_info_pokemon(self, ecran, font, mon_pokemon, adversaire):
        # Informations sur votre Pokémon
        info_mon_pokemon = font.render(f"{mon_pokemon.nom} PV: {mon_pokemon.pv}", True, (0, 0, 0))
        cadre_texte_mon_pokemon = pygame.image.load("images/cadre_texte/cadre_texte_combat.png").convert_alpha()
        ecran.blit(cadre_texte_mon_pokemon, (30, 200))
        ecran.blit(info_mon_pokemon, (70, 215))

        # Informations sur le Pokémon adverse
        info_adversaire = font.render(f"{adversaire.nom} PV: {adversaire.pv}", True, (0, 0, 0))
        cadre_texte_adversaire = pygame.image.load("images/cadre_texte/cadre_texte_combat.png").convert_alpha()
        ecran.blit(cadre_texte_adversaire, (500, 20))
        ecran.blit(info_adversaire, (550, 40))


    def gerer_action_bouton_fuite(self, ecran):
        print(f"{self.mon_pokemon.nom} a fui le combat.")
        pygame.mixer.music.stop()
        self.running = False



    def gerer_attaque_adversaire(self, ecran):
        message = self.effectuer_attaque(self.adversaire, self.mon_pokemon)
        # Afficher le message sur l'écran
        self.tour_mon_pokemon = True

    def effectuer_attaque(self, attaquant, defenseur):
        if random.random() <= 0.05:  # 5% de chance de rater
            message = f"{attaquant.nom} a raté son attaque."

        elif random.random() <= 0.05:

            degats = self.calculer_degats(attaquant, attaquant.attaque_de_base, defenseur) 
            degats = int(degats)*2
            self.appliquer_degats(defenseur, degats)
            message = f"{attaquant.nom} fait une attaque critique et inflige {int(degats)} dégâts à {defenseur.nom}."

        else:
            degats = self.calculer_degats(attaquant, attaquant.attaque_de_base, defenseur)
            self.appliquer_degats(defenseur, degats)
            message = f"{attaquant.nom} attaque {attaquant.attaque_de_base.nom} et inflige {int(degats)} dégâts à {defenseur.nom}."
        return message