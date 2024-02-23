import json
from classes.Type import *
from classes.Attaque import *

class Pokemon:
    tous_pokemons = []  # Attribut de classe pour stocker tous les Pokémon chargés

    def __init__(self, nom, type_pokemon, pv, attaque, defense, lvl, xp, xp_necessaire, attaque_de_base=None):
        self.nom = nom
        self.type = type_pokemon
        self.pv = pv
        self.pv_max = pv
        self.attaque = attaque
        self.defense = defense
        self.lvl = lvl
        self.xp = xp
        self.xp_necessaire = xp_necessaire
        self.attaque_de_base = attaque_de_base


        Pokemon.tous_pokemons.append(self)  # Ajout du Pokémon nouvellement créé à la liste de tous les Pokémon

    @staticmethod
    def import_json(filename):
        with open(filename, 'r') as file:
            data = json.load(file)

        for donnee_pokemon in data:
            type_pokemon = getattr(Type, donnee_pokemon['type'].lower())()
            pokemon = Pokemon(
                nom=donnee_pokemon['nom'],
                type_pokemon=type_pokemon,
                pv=donnee_pokemon['pv'],
                attaque=donnee_pokemon['attaque'],
                defense=donnee_pokemon['defense'],
                lvl=donnee_pokemon['lvl'],
                xp=donnee_pokemon['xp'],
                xp_necessaire=donnee_pokemon['xp_necessaire']  
                )
        # L'ajout à tous_pokemons se fait dans le __init__

        return Pokemon.tous_pokemons  # Retour de la liste complète des Pokémon chargés

    def soigner(self):
        self.pv = self.pv_max  # Méthode pour soigner le Pokémon à ses PV max

    def __str__(self):
        return f"{self.nom} ({self.type.nom}) - PV: {self.pv} Attaque: {self.attaque} Défense: {self.defense} Niveau: {self.lvl} XP: {self.xp}"
    
    def gagner_xp(self, quantite):
        self.xp += quantite
        while self.xp >= self.xp_necessaire:
            self.monter_de_niveau()
    
    def monter_de_niveau(self):
        self.xp -= self.xp_necessaire
        self.lvl += 1
        self.xp_necessaire *= 1.2  # Augmenter le seuil pour le prochain niveau
        self.pv_max += 10  # Augmenter les PV max
        self.pv = self.pv_max  # Soigner le Pokémon à ses nouveaux PV max
        self.attaque += 5  # Augmenter l'attaque
        self.defense += 5  # Augmenter la défense
        nouvelle_attaque = Attaque.assigner_attaque_base(self)
        if nouvelle_attaque.nom != self.attaque_de_base.nom:
            self.attaque_de_base = nouvelle_attaque
            print(f"{self.nom} est monté au niveau {self.lvl} et a appris une nouvelle attaque : {self.attaque_de_base.nom}!")
        else:
            print(f"{self.nom} est monté au niveau {self.lvl}")

        if self.lvl == 7:
            evolution = f"evolution_{self.nom.lower()}"
            getattr(self, evolution)()


    def evolution_salameche(self):
        print(f"{self.nom} évolue en Reptincel!")
        self.nom = "Reptincel"
        self.pv_max += 20
        self.attaque += 10
        self.defense += 10
        self.pv = self.pv_max

    def evolution_carapuce(self):
        print(f"{self.nom} évolue en Carabaffe!")
        self.nom = "Carabaffe"
        self.pv_max += 20
        self.attaque += 15
        self.defense += 10
        self.pv = self.pv_max

    def evolution_bulbizarre(self):
        print(f"{self.nom} évolue en Herbizarre!")
        self.nom = "Herbizarre"
        self.pv_max += 20
        self.attaque += 10
        self.defense += 15
        self.pv = self.pv_max

    def evolution_pikachu(self):
        print(f"{self.nom} évolue en Raichu!")
        self.nom = "Raichu"
        self.pv_max += 20
        self.attaque += 10
        self.defense += 10
        self.pv = self.pv_max

    def evolution_evoli(self):
        print(f"{self.nom} évolue en Voltali!")
        self.nom = "Phyllali"
        self.pv_max += 20
        self.attaque += 10
        self.defense += 10
        self.pv = self.pv_max

    def evolution_rattata(self):
        print(f"{self.nom} évolue en Rattatac!")
        self.nom = "Rattatac"
        self.pv_max += 20
        self.attaque += 10
        self.defense += 10
        self.pv = self.pv_max

    def evolution_roucool(self):
        print(f"{self.nom} évolue en Roucoups!")
        self.nom = "Roucoups"
        self.pv_max += 20
        self.attaque += 10
        self.defense += 10
        self.pv = self.pv_max

    def evolution_osselait(self):
        print(f"{self.nom} évolue en Ossatueur!")
        self.nom = "Ossatueur"
        self.pv_max += 20
        self.attaque += 10
        self.defense += 10
        self.pv = self.pv_max