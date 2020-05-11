from id3 import ID3
from traitement import traitement_donnees

class ResultValues():

    def __init__(self):

        # Do computations here
        donnee_train = import_donnee("../Data/train_bin.csv")
        arbre_recursif = construit_arbre_recur(donnee_train)
        print(arbre_recursif)
        print('hello')
        # Task 1
        self.arbre = None
        # Task 3
        self.faits_initiaux = None
        self.regles = None
        # Task 5
        self.arbre_advance = None

    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]
