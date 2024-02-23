from classes.Type import Type

class Attaque:
    def __init__(self, nom, puissance, type_attaque):
        self.nom = nom
        self.puissance = puissance
        self.type = type_attaque

    @staticmethod
    def attaque_feu(niveau):
        if niveau < 8:
            return Attaque("Flammèche", 40, Type.feu())
        else:
            return Attaque("Lance-Flamme", 90, Type.feu())
        
    @staticmethod
    def attaque_eau(niveau):
        if niveau < 8:
            return Attaque("Pistolet à O", 40, Type.eau())
        else:
            return Attaque("Hydrocanon", 90, Type.eau())
        
    @staticmethod
    def attaque_electrik(niveau):
        if niveau < 8:
            return Attaque("Eclair", 40, Type.electrik())
        else:
            return Attaque("Fatal-Foudre", 90, Type.electrik())
        
    @staticmethod
    def attaque_plante(niveau):
        if niveau < 8:
            return Attaque("Tranch'Herbe", 40, Type.plante())
        else:
            return Attaque("Lance-Soleil", 90, Type.plante())
        
    @staticmethod
    def attaque_normal(niveau):
        if niveau < 8:
            return Attaque("Charge", 40, Type.normal())
        else:
            return Attaque("Damoclès", 90, Type.normal())
        
    @staticmethod
    def attaque_vol(niveau):
        if niveau < 8:
            return Attaque("Picpic", 40, Type.vol())
        else:
            return Attaque("Rapace", 90, Type.vol())
        
    @staticmethod
    def attaque_poison(niveau):
        if niveau < 8:
            return Attaque("Dard-Venin", 40, Type.poison())
        else:
            return Attaque("Bomb-Beurk", 90, Type.poison())
        
    @staticmethod
    def attaque_sol(niveau):
        if niveau < 8:
            return Attaque("Tunnel", 40, Type.sol())
        else:
            return Attaque("Séisme", 90, Type.sol())
        
    @staticmethod
    def attaque_roche(niveau):
        if niveau < 8:
            return Attaque("Roulade", 40, Type.roche())
        else:
            return Attaque("Lame de Roc", 90, Type.roche())
        
    @staticmethod
    def attaque_spectre(niveau):
        if niveau < 8:
            return Attaque("Griffe Ombre", 40, Type.spectre())
        else:
            return Attaque("Ball'Ombre", 90, Type.spectre())
        
    @staticmethod
    def attaque_acier(niveau):
        if niveau < 8:
            return Attaque("Plaie-Croix", 40, Type.acier())
        else:
            return Attaque("Luminocanon", 90, Type.acier())
        
    @staticmethod
    def attaque_insecte(niveau):
        if niveau < 8:
            return Attaque("Taillade", 40, Type.insecte())
        else:
            return Attaque("Bourdon", 90, Type.insecte())
        
    @staticmethod
    def attaque_combat(niveau):
        if niveau < 8:
            return Attaque("Balayette", 40, Type.combat())
        else:
            return Attaque("Close Combat", 90, Type.combat())
        
    @staticmethod
    def attaque_psy(niveau):
        if niveau < 8:
            return Attaque("Choc Mental", 40, Type.psy())
        else:
            return Attaque("Psyko", 90, Type.psy())
        
    @classmethod
    def assigner_attaque_base(cls, pokemon ):
        # Configuration de l'attaque de base du Pokémon en fonction de son type et du niveau du Pokémon
        type_pokemon = pokemon.type.nom.lower()
        niveau = pokemon.lvl
        method_name = f'attaque_{type_pokemon}'
    
        if hasattr(cls, method_name):
            return getattr(cls, method_name)(niveau)
        else:
            return None