class Type:
    def __init__(self, nom, forces=[], faiblesses=[], nulle_defense=[]):
        self.nom = nom
        self.forces = forces
        self.faiblesses = faiblesses
        self.nulle_defense = nulle_defense

    @staticmethod
    def feu():
        return Type("Feu", forces=["Plante", "Glace", "Insecte", "Acier"], faiblesses=["Eau", "Roche", "Sol"])

    @staticmethod
    def eau():
        return Type("Eau", forces=["Feu", "Sol", "Roche"], faiblesses=["Plante", "Electrik"])

    @staticmethod
    def plante():
        return Type("Plante", forces=["Eau", "Sol", "Roche"], faiblesses=["Feu", "Glace", "Poison", "Vol", "Insecte"])

    @staticmethod
    def electrik():
        return Type("Electrik", forces=["Eau", "Vol","Electrik"], faiblesses=["Sol"])

    @staticmethod
    def glace():
        return Type("Glace", forces=["Plante", "Sol", "Vol", "Dragon"], faiblesses=["Feu", "Combat", "Roche", "Acier"])

    @staticmethod
    def combat():
        return Type("Combat", forces=["Normal", "Glace", "Roche", "Ténèbres", "Acier"], faiblesses=["Vol", "Psy", "Fée"])

    @staticmethod
    def poison():
        return Type("Poison", forces=["Plante", "Fée"], faiblesses=["Sol", "Psy"], nulle_defense=["Acier"])

    @staticmethod
    def sol():
        return Type("Sol", forces=["Feu", "Electrik", "Poison", "Roche", "Acier"], faiblesses=["Eau", "Plante", "Glace"])

    @staticmethod
    def vol():
        return Type("Vol", forces=["Plante", "Combat", "Insecte"], faiblesses=["Electrik", "Glace", "Roche"], nulle_defense=["Sol"])

    @staticmethod
    def psy():
        return Type("Psy", forces=["Combat", "Poison"], faiblesses=["Insecte", "Ténèbres", "Spectre"])

    @staticmethod
    def insecte():
        return Type("Insecte", forces=["Plante", "Psy", "Ténèbres"], faiblesses=["Feu", "Vol", "Roche"])

    @staticmethod
    def roche():
        return Type("Roche", forces=["Feu", "Glace", "Vol", "Insecte"], faiblesses=["Eau", "Plante", "Combat", "Sol", "Acier"])

    @staticmethod
    def spectre():
        return Type("Spectre", forces=["Psy", "Spectre"], faiblesses=["Spectre", "Ténèbres"], nulle_defense=["Normal", "Combat"])

    @staticmethod
    def dragon():
        return Type("Dragon", forces=["Dragon"], faiblesses=["Glace", "Dragon", "Fée"])

    @staticmethod
    def tenebres():
        return Type("Ténèbres", forces=["Psy", "Spectre"], faiblesses=["Combat", "Insecte", "Fée"], nulle_defense=["Psy"])

    @staticmethod
    def acier():
        return Type("Acier", forces=["Glace", "Roche", "Fée"], faiblesses=["Feu", "Combat", "Sol"])

    @staticmethod
    def fee():
        return Type("Fée", forces=["Combat", "Dragon", "Ténèbres"], faiblesses=["Poison", "Acier"])
    
    @staticmethod
    def normal():
        return Type("Normal", forces=[], faiblesses=["Combat"], nulle_defense=["Spectre"])