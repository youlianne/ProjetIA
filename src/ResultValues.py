from id3 import ID3
from traitement import traitement_donnees

class ResultValues():

    def __init__(self):
        id3 = ID3()
        # Do computations here
        donnee_train = traitement_donnees.import_donnee(self,"../Data/train_bin.csv")
        donnee_test = traitement_donnees.import_donnee_test(self,"../Data/test_public_bin.csv")
        # Task 1
        self.arbre = id3.construit_arbre(donnee_train)
        #print(self.arbre)

        n = 0
        p = 0
        for donnee in donnee_test :
            model_result = self.arbre.classifie(donnee)
            if model_result[-1] == donnee['target']:
                p = p+1
            n = n+1
        print("Precision : ")
        print(p/n)
        # Task 3
        self.faits_initiaux = None
        self.regles = self.arbre.generation_regle()
            # Affichage des règles
        r = 0
        for regle in self.regles:
            r += 1
            print(str(r) + ') ' + self.arbre.ecrit_regle(regle))
            # Justification d'un exemple à l'aide des règles
        #for ex in donnee_test:
        print(self.arbre.justifie_exemple(donnee_test[2], self.regles))
        # Task 5
        self.arbre_advance = None

    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]
