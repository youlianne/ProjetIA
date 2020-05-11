from id3 import ID3
from traitement import traitement_donnees

class ResultValues():

    def __init__(self):
        id3 = ID3()
        # Do computations here
        donnee_train = traitement_donnees.import_donnee(self,"../Data/train_bin.csv")
        
        arbre = id3.construit_arbre(donnee_train)
        print(arbre)
        # Task 1
        self.arbre = None
        # Task 3
        self.faits_initiaux = None
        self.regles = None
        # Task 5
        self.arbre_advance = None

    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]
